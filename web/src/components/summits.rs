use anyhow::Context;
use yew::{function_component, html, use_context, Html};

use crate::{helpers::catch::catch, views::summit::summit_brief};

#[function_component(Summits)]
pub fn component() -> Html {
    let summits =
        use_context::<Vec<crate::model::summit::Summit>>().context("Summits context is missing");

    catch(|| {
        Ok(html! {
            <>
                <ul>
                    { summits?.iter().map(|s|{
                    html!{
                        <li>
                        {summit_brief(s)}
                        </li>
                    }
                }).collect::<Html>() }
                </ul>
            </>
        })
    })
}
