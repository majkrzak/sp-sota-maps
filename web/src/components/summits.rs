use anyhow::Context;
use yew::{function_component, html, use_context, Html};

use crate::{helpers::catch::catch, views::summit::summit_brief};

#[function_component(Summits)]
pub fn component() -> Html {
    let summits =
        use_context::<crate::model::summits::Summits>().context("Summits context is missing");

    catch(|| {
        Ok(html! {
            <>
                <ul>
                    { summits?.iter().map(|summit|{
                    html!{
                        <li key={summit.reference.slug()}>
                        {summit_brief(summit)}
                        </li>
                    }
                }).collect::<Html>() }
                </ul>
            </>
        })
    })
}
