use anyhow::Context;
use yew::{function_component, html, use_context, Html, Properties};

use crate::{
    helpers::catch::catch,
    model::{reference::Reference, release::Release, summits::Summits},
    views::summit::{summit_brief, summit_downloads, summit_image, summit_links},
};

#[derive(Properties, PartialEq, Clone)]
pub struct Props {
    pub reference: Reference,
}

#[function_component(SummitDetails)]
pub fn component(props: &Props) -> Html {
    let summits = use_context::<Summits>().context("Summits context is missing.");
    let release = use_context::<Release>().context("Release context is missing.");

    catch(|| {
        let summit = summits?.get(&props.reference).context("Summit not found")?;
        let release = release?;
        Ok(html! {
            <article>
                <h3>{ summit_brief(&summit) }</h3>
                <nav>{ summit_links(&summit) }</nav>
                { summit_image(&release, &summit) }
                <section>
                    <h4>{ "Downloads" }</h4>
                    <nav>{ summit_downloads(&release, &summit) }</nav>
                </section>
            </article>
        })
    })
}
