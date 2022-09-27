use crate::rpm_ostree::TransactionProxy;
use async_signals::Signals;
use async_std::stream::StreamExt;
use futures_util::join;
use indicatif::{ProgressBar, ProgressStyle};
use std::{
    cell::RefCell,
    os::unix::net::{SocketAddr, UnixStream},
    process::exit,
    time::Duration,
};

pub async fn handle_transaction(transaction: &TransactionProxy<'_>) -> Result<(), zbus::Error> {
    let mut receive_message = transaction.receive_message().await?;
    let mut receive_percent_progress = transaction.receive_percent_progress().await?;
    let mut receive_download_progress = transaction.receive_download_progress().await?;
    let mut receive_progress_end = transaction.receive_progress_end().await?;
    let mut receive_task_begin = transaction.receive_task_begin().await?;
    let mut receive_task_end = transaction.receive_task_end().await?;
    let mut receive_finished = transaction.receive_finished().await?;

    let mut signals = Signals::new(vec![2, 15]).unwrap();

    let bar: RefCell<Option<ProgressBar>> = RefCell::new(None);

    join!(
        async {
            while let Some(_) = receive_message.next().await {
                // let args = message.args().unwrap();
                // println!("{}", args.text);
            }
        },
        async {
            while let Some(message) = receive_percent_progress.next().await {
                if bar.borrow().is_none() {
                    let new_bar = indicatif::ProgressBar::new(100);
                    new_bar.set_style(
                        ProgressStyle::with_template(&format!(
                            "{{prefix:.bold}}{{bar:20}} {{msg}}"
                        ))
                        .unwrap()
                        .progress_chars("█▓▒░  "),
                    );
                    bar.replace(Some(new_bar));
                }

                let args = message.args().unwrap();
                let text = args.text.to_string();
                let bar = bar.borrow();
                let bar = bar.as_ref().unwrap();
                bar.set_position(args.percentage.into());
                bar.set_message(text);
            }
        },
        async {
            while let Some(_) = receive_download_progress.next().await {
                // println!("{:#?}", message.args().unwrap().time());
            }
        },
        async {
            while let Some(_message) = receive_progress_end.next().await {
                let old_bar = bar.take().unwrap();
                old_bar.finish();
            }
        },
        async {
            while let Some(message) = receive_task_begin.next().await {
                let args = message.args().unwrap();
                let new_bar = indicatif::ProgressBar::new_spinner();
                new_bar.enable_steady_tick(Duration::from_millis(120));
                new_bar.set_style(
                    ProgressStyle::with_template("{spinner} {msg}")
                        .unwrap()
                        .tick_strings(&[
                            "█▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁",
                            "██▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁",
                            "███▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁",
                            "████▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁",
                            "██████▁▁▁▁▁▁▁▁▁▁▁▁▁▁",
                            "██████▁▁▁▁▁▁▁▁▁▁▁▁▁▁",
                            "███████▁▁▁▁▁▁▁▁▁▁▁▁▁",
                            "████████▁▁▁▁▁▁▁▁▁▁▁▁",
                            "█████████▁▁▁▁▁▁▁▁▁▁▁",
                            "█████████▁▁▁▁▁▁▁▁▁▁▁",
                            "██████████▁▁▁▁▁▁▁▁▁▁",
                            "███████████▁▁▁▁▁▁▁▁▁",
                            "█████████████▁▁▁▁▁▁▁",
                            "██████████████▁▁▁▁▁▁",
                            "██████████████▁▁▁▁▁▁",
                            "▁██████████████▁▁▁▁▁",
                            "▁██████████████▁▁▁▁▁",
                            "▁██████████████▁▁▁▁▁",
                            "▁▁██████████████▁▁▁▁",
                            "▁▁▁██████████████▁▁▁",
                            "▁▁▁▁█████████████▁▁▁",
                            "▁▁▁▁██████████████▁▁",
                            "▁▁▁▁██████████████▁▁",
                            "▁▁▁▁▁██████████████▁",
                            "▁▁▁▁▁██████████████▁",
                            "▁▁▁▁▁██████████████▁",
                            "▁▁▁▁▁▁██████████████",
                            "▁▁▁▁▁▁██████████████",
                            "▁▁▁▁▁▁▁█████████████",
                            "▁▁▁▁▁▁▁█████████████",
                            "▁▁▁▁▁▁▁▁████████████",
                            "▁▁▁▁▁▁▁▁████████████",
                            "▁▁▁▁▁▁▁▁▁███████████",
                            "▁▁▁▁▁▁▁▁▁███████████",
                            "▁▁▁▁▁▁▁▁▁▁██████████",
                            "▁▁▁▁▁▁▁▁▁▁██████████",
                            "▁▁▁▁▁▁▁▁▁▁▁▁████████",
                            "▁▁▁▁▁▁▁▁▁▁▁▁▁███████",
                            "▁▁▁▁▁▁▁▁▁▁▁▁▁▁██████",
                            "▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁█████",
                            "▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁█████",
                            "█▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁████",
                            "██▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁███",
                            "██▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁███",
                            "███▁▁▁▁▁▁▁▁▁▁▁▁▁▁███",
                            "████▁▁▁▁▁▁▁▁▁▁▁▁▁▁██",
                            "█████▁▁▁▁▁▁▁▁▁▁▁▁▁▁█",
                            "█████▁▁▁▁▁▁▁▁▁▁▁▁▁▁█",
                            "██████▁▁▁▁▁▁▁▁▁▁▁▁▁█",
                            "████████▁▁▁▁▁▁▁▁▁▁▁▁",
                            "█████████▁▁▁▁▁▁▁▁▁▁▁",
                            "█████████▁▁▁▁▁▁▁▁▁▁▁",
                            "█████████▁▁▁▁▁▁▁▁▁▁▁",
                            "█████████▁▁▁▁▁▁▁▁▁▁▁",
                            "███████████▁▁▁▁▁▁▁▁▁",
                            "████████████▁▁▁▁▁▁▁▁",
                            "████████████▁▁▁▁▁▁▁▁",
                            "██████████████▁▁▁▁▁▁",
                            "██████████████▁▁▁▁▁▁",
                            "▁██████████████▁▁▁▁▁",
                            "▁██████████████▁▁▁▁▁",
                            "▁▁▁█████████████▁▁▁▁",
                            "▁▁▁▁▁████████████▁▁▁",
                            "▁▁▁▁▁████████████▁▁▁",
                            "▁▁▁▁▁▁███████████▁▁▁",
                            "▁▁▁▁▁▁▁▁█████████▁▁▁",
                            "▁▁▁▁▁▁▁▁█████████▁▁▁",
                            "▁▁▁▁▁▁▁▁▁█████████▁▁",
                            "▁▁▁▁▁▁▁▁▁█████████▁▁",
                            "▁▁▁▁▁▁▁▁▁▁█████████▁",
                            "▁▁▁▁▁▁▁▁▁▁▁████████▁",
                            "▁▁▁▁▁▁▁▁▁▁▁████████▁",
                            "▁▁▁▁▁▁▁▁▁▁▁▁███████▁",
                            "▁▁▁▁▁▁▁▁▁▁▁▁███████▁",
                            "▁▁▁▁▁▁▁▁▁▁▁▁▁███████",
                            "▁▁▁▁▁▁▁▁▁▁▁▁▁███████",
                            "▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁█████",
                            "▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁████",
                            "▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁████",
                            "▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁████",
                            "▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁███",
                            "▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁███",
                            "▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁██",
                            "▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁██",
                            "▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁██",
                            "▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁█",
                            "▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁█",
                            "▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁█",
                            "▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁",
                            "▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁",
                            "▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁",
                            "▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁▁",
                        ]),
                );
                new_bar.set_message(args.text.to_string());

                bar.replace(Some(new_bar));
                // println!("{}", args.text);
            }
        },
        async {
            while let Some(_) = receive_task_end.next().await {
                let bar = bar.take().unwrap();
                bar.finish();
            }
        },
        async {
            let message = receive_finished.next().await.unwrap();
            let args = message.args().unwrap();
            if !args.success {
                println!("{}", args.error_message);
                exit(1)
            } else {
                exit(0)
            }
        },
        async {
            while let Some(signal) = signals.next().await {
                println!("Signal: {}", signal);
                transaction.cancel().await.unwrap();
            }
        }
    );

    Ok(())
}

pub async fn get_transaction(transaction_address: &str) -> Result<TransactionProxy, zbus::Error> {
    let addr = SocketAddr::from_abstract_namespace(
        transaction_address
            .strip_prefix("unix:abstract=")
            .expect("Failed to parse Unix stream connection address")
            .as_bytes(),
    )?;
    let stream = UnixStream::connect_addr(&addr)?;

    let transaction_connection = zbus::ConnectionBuilder::unix_stream(stream)
        .p2p()
        .build()
        .await?;
    let transaction = TransactionProxy::builder(&transaction_connection)
        .path("/")?
        .build()
        .await?;

    Ok(transaction)
}
