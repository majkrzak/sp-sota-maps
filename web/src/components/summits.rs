use yew::{function_component, html, use_context, Html};

use crate::components::summit_brief::SummitBrief;

#[function_component(Summits)]
pub fn component() -> Html {
    let summits = use_context::<Vec<crate::model::summit::Summit>>().unwrap();

    html! {
        <>
            <ul>
                {
                    summits.iter().map(|summit| {
                        html!{
                            <SummitBrief reference={summit.reference.clone()}/>
                        }
                    }).collect::<Html>()
                }
            </ul>
        </>
    }
}
