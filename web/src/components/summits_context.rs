use base64::{prelude::BASE64_STANDARD, Engine};
use yew::{function_component, html, use_context, ContextProvider, Html, HtmlResult, Properties};

use crate::model::{release::Release, summit::Summit};

#[derive(Properties, PartialEq, Clone)]
pub struct Props {
    pub children: Html,
}

#[function_component(SummitsContext)]
pub fn component(props: &Props) -> HtmlResult {
    let release = use_context::<Release>().expect("no release context");

    let mut reader = std::io::Cursor::new(
        BASE64_STANDARD
            .decode(release.body.replace(&['`', '\n', '\r'], ""))
            .expect("not valid base64"),
    );
    let mut decomp: Vec<u8> = Vec::new();

    lzma_rs::xz_decompress(&mut reader, &mut decomp).expect("not an lzma");

    let json_string = String::from_utf8(decomp).expect("not a UTF8 string");

    let summits: Vec<Summit> = serde_json::from_str(json_string.as_str()).expect("not valid json");

    Ok(html! {
        <ContextProvider<Vec<Summit>> context={summits.clone()}>
            { props.children.clone() }
        </ContextProvider<Vec<Summit>>>
    })
}
