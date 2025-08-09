use anyhow::Context;
use yew::{function_component, html, use_context, Html};

use crate::{helpers::catch::catch, model::release::Release};

#[function_component(Footer)]
pub fn component() -> Html {
    let release = use_context::<Release>().context("Release context is missing.");

    catch(|| {
        let release = release?;
        Ok(html! {
            <footer>
                <p>
                    { "SP-SOTA-MAPS © 2025 Piotr Majkrzak" }
                    <br />
                    <a href="https://github.com/majkrzak/sp-sota-maps">
                        { "majkrzak/sp-sota-maps" }
                    </a>
                    <br/>
                    { release.name }
                </p>
            </footer>
        })
    })
}
