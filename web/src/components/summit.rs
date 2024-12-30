use yew::{function_component, html, Html, Properties};

use crate::model::reference::Reference;

#[derive(Properties, PartialEq)]
pub struct Props {
    pub reference: Reference,
}

#[function_component(Summit)]
pub fn component(props: &Props) -> Html {
    html! {
        <>
            {props.reference.full()}
        </>
    }
}
