use anyhow::Context;
use yew::{function_component, html, use_context, Html, Properties};

use crate::{
    helpers::catch::catch,
    model::{reference::Reference, release::Release, summit::Summit, summits::Summits},
    views::summit::summit_brief,
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
                <nav>
                    <a
                        style="margin:0 .5em"
                        href={format!("https://www.sotadata.org.uk/summit/{}",summit.reference.full())}
                    >
                        { "sotadata.org.uk" }
                    </a>
                    <a
                        style="margin:0 .5em"
                        href={format!("https://sotl.as/summits/{}",summit.reference.full())}
                    >
                        { "sotl.as" }
                    </a>
                </nav>
                <img
                    src={release.asset(format!("{}.avif",summit.reference.slug()).as_str()).unwrap().browser_download_url.clone()}
                />
                <section>
                    <h4>{ "Downloads" }</h4>
                    <nav>
                        <a
                            class="button"
                            style="margin:0 .5em"
                            href={release.asset(format!("{}.pdf",summit.reference.slug()).as_str()).unwrap().browser_download_url.clone()}
                        >
                            { "A5 PDF" }
                        </a>
                        <a
                            class="button"
                            style="margin:0 .5em"
                            href={release.asset(format!("{}.png",summit.reference.slug()).as_str()).unwrap().browser_download_url.clone()}
                        >
                            { "1440p PNG" }
                        </a>
                        <a
                            class="button"
                            style="margin:0 .5em"
                            href={release.asset(format!("{}.avif",summit.reference.slug()).as_str()).unwrap().browser_download_url.clone()}
                        >
                            { "1440p AVIF" }
                        </a>
                    </nav>
                </section>
            </article>
        })
    })
}
