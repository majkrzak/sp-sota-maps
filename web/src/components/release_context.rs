use anyhow::Context;
use gloo_net::http::Request;
use yew::{
    function_component, html, suspense::use_future, ContextProvider, Html, HtmlResult, Properties,
};

use crate::{model::release::Release, views::error::error};

#[derive(Properties, PartialEq, Clone)]
pub struct Props {
    pub children: Html,
}

#[function_component(ReleaseContext)]
pub fn component(props: &Props) -> HtmlResult {
    match *use_future(|| async {
        Request::get("https://api.github.com/repos/majkrzak/sp-sota-maps/releases/latest")
            .send()
            .await
            .context("can not fetch release data")?
            .json::<Release>()
            .await
            .context("can not parse release data")
    })? {
        Ok(ref release) => Ok(html! {
            <ContextProvider<Release> context={release.clone()}>
                { props.children.clone() }
            </ContextProvider<Release>>
        }),
        Err(ref e) => Ok(error(e)),
    }
}
