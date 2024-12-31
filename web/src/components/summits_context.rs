use std::io;

use gloo_net::http::Request;
use serde::de::DeserializeOwned;
use yew::{
    function_component, html, suspense::use_future, use_context, ContextProvider, Html, HtmlResult,
    Properties,
};

use crate::model::release::Release;

#[derive(Properties, PartialEq, Clone)]
pub struct Props {
    pub children: Html,
}

#[function_component(SummitsContext)]
pub fn component(props: &Props) -> HtmlResult {
    let release = use_context::<Release>().expect("no release context");

    match *use_future(|| async move {
        let data = Request::get(format!("https://api.allorigins.win/raw?url=https://github.com/majkrzak/sp-sota-maps/releases/download/{}/_summits.csv", release.tag_name).as_str())
            .send()
            .await?
            .text()
            .await?;

        fn parse_csv<D: DeserializeOwned, R: io::Read>(rdr: R) -> csv::Result<Vec<D>> {
            csv::Reader::from_reader(rdr).into_deserialize().collect()
        }

        let summits = parse_csv(data.as_bytes())?;

        <Result<Vec<crate::model::summit::Summit>, anyhow::Error>>::Ok(summits)
    })? {
        Ok(ref summits) => Ok(html! {
            <ContextProvider<Vec<crate::model::summit::Summit>> context={summits.clone()}>
                { props.children.clone() }
            </ContextProvider<Vec<crate::model::summit::Summit>>>
        }),
        Err(_) => Ok(html! {{"ERROR"}}),
    }
}
