#![feature(unix_socket_abstract)]

use clap::{Parser, Subcommand};
use rpm_ostree::{OSProxy, SysrootProxy};
use std::collections::HashMap;
use zbus::Connection;

mod rpm_ostree;
mod transaction;

#[derive(Parser)]
#[clap(author, version, about, long_about = None)]
struct Cli {
    #[clap(subcommand)]
    command: Commands,
}

#[derive(Subcommand)]
enum Commands {
    Install { name: Vec<String> },
    Remove { name: Vec<String> },
    Search { name: String },
    Info { name: String },
    Update {},
}

async fn get_os_proxy<'a>(sysroot: &'a SysrootProxy<'a>) -> Result<OSProxy<'a>, zbus::Error> {
    let os_path = sysroot.booted().await?;

    let proxy = rpm_ostree::OSProxy::builder(sysroot.connection())
        .destination("org.projectatomic.rpmostree1")?
        .path(os_path)?
        .build()
        .await?;

    Ok(proxy)
}

#[tokio::main]
async fn main() -> anyhow::Result<()> {
    let cli = Cli::parse();

    let connection = Connection::system().await?;
    match &cli.command {
        Commands::Install { name } => {
            let sysroot = rpm_ostree::SysrootProxy::new(&connection).await?;
            let proxy = get_os_proxy(&sysroot).await?;

            let packages = name.iter().map(|s| s.as_str()).collect::<Vec<&str>>();
            let transaction_address = proxy
                .pkg_change(HashMap::new(), packages.as_slice(), &[])
                .await?;

            let transaction = transaction::get_transaction(&transaction_address).await?;
            transaction.start().await?;
            transaction::handle_transaction(&transaction).await?;
        }
        Commands::Remove { name } => {
            let sysroot = rpm_ostree::SysrootProxy::new(&connection).await?;
            let proxy = get_os_proxy(&sysroot).await?;

            let packages = name.iter().map(|s| s.as_str()).collect::<Vec<&str>>();
            let transaction_address = proxy
                .pkg_change(HashMap::new(), &[], packages.as_slice())
                .await?;

            let transaction = transaction::get_transaction(&transaction_address).await?;
            transaction.start().await?;
            transaction::handle_transaction(&transaction).await?;
        }
        Commands::Update {} => {
            let sysroot = rpm_ostree::SysrootProxy::new(&connection).await?;
            let proxy = get_os_proxy(&sysroot).await?;

            let transaction_address = proxy.upgrade(HashMap::new()).await?;

            let transaction = transaction::get_transaction(&transaction_address).await?;
            transaction.start().await?;
            transaction::handle_transaction(&transaction).await?;
        }
        Commands::Search { name: _ } => {}
        Commands::Info { name: _ } => {}
    }

    Ok(())
}
