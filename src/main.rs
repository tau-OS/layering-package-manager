#![feature(unix_socket_abstract)]

use clap::{Parser, Subcommand};
use rpm_ostree::{OSProxyBlocking, SysrootProxyBlocking};
use std::{collections::HashMap, ffi::OsString, process::exit};
use zbus::blocking::Connection;

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

fn get_os_proxy<'a>(
    sysroot: &'a SysrootProxyBlocking<'a>,
) -> Result<OSProxyBlocking<'a>, zbus::Error> {
    let os_path = sysroot.booted()?;

    let proxy = rpm_ostree::OSProxyBlocking::builder(sysroot.connection())
        .destination("org.projectatomic.rpmostree1")?
        .path(os_path)?
        .build()?;

    Ok(proxy)
}

#[async_std::main]
async fn main() -> anyhow::Result<()> {
    let cli = Cli::parse();

    let connection = Connection::system()?;
    match &cli.command {
        Commands::Install { name } => {
            let sysroot = rpm_ostree::SysrootProxyBlocking::new(&connection)?;
            let proxy = get_os_proxy(&sysroot)?;

            let packages = name.iter().map(|s| s.as_str()).collect::<Vec<&str>>();
            let transaction_address = proxy.pkg_change(HashMap::new(), packages.as_slice(), &[])?;

            let transaction = transaction::get_transaction(&transaction_address).await?;
            transaction.start().await?;
            transaction::handle_transaction(&transaction).await?;
        }
        Commands::Remove { name } => {
            let sysroot = rpm_ostree::SysrootProxyBlocking::new(&connection)?;
            let proxy = get_os_proxy(&sysroot)?;

            let packages = name.iter().map(|s| s.as_str()).collect::<Vec<&str>>();
            let transaction_address = proxy.pkg_change(HashMap::new(), &[], packages.as_slice())?;

            let transaction = transaction::get_transaction(&transaction_address).await?;
            transaction.start().await?;
            transaction::handle_transaction(&transaction).await?;
        }
        Commands::Update {} => {
            let sysroot = rpm_ostree::SysrootProxyBlocking::new(&connection)?;
            let proxy = get_os_proxy(&sysroot)?;

            let transaction_address = proxy.upgrade(HashMap::new())?;

            let transaction = transaction::get_transaction(&transaction_address).await?;
            transaction.start().await?;
            transaction::handle_transaction(&transaction).await?;
        }
        Commands::Search { name } => {}
        Commands::Info { name } => {}
    }

    Ok(())
}
