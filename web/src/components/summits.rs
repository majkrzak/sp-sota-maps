use yew::{function_component, html, use_context, Html};

use crate::views::summit::summit_brief;

#[function_component(Summits)]
pub fn component() -> Html {
    let summits = use_context::<Vec<crate::model::summit::Summit>>().unwrap();

    html! {
        <>
            <ul>{ summits.iter().map(summit_brief).collect::<Html>() }</ul>
        </>
    }
}
