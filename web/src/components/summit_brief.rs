use yew::{function_component, html, use_context, Html, Properties};
use yew_router::prelude::Link;

use crate::{
    model::{reference::Reference, summit::Summit},
    router::Route,
};

#[derive(Properties, PartialEq, Clone)]
pub struct Props {
    pub reference: Reference,
}

#[function_component(SummitBrief)]
pub fn component(props: &Props) -> Html {
    match use_context::<Vec<Summit>>()
        .expect("no ctx")
        .iter()
        .find(|x| x.reference == props.reference)
    {
        Some(summit) => html! {
            <p>
                <Link<Route> to={Route::Summit{reference:summit.reference.clone()}}>
                    {summit.reference.full()}
                    {", "}
                    {summit.name.clone()}
                    {" – "}
                    {format!("{:0.0}m",summit.alt)}
                </Link<Route>>
            </p>
        },
        None => html! {{"todo"}},
    }
}
