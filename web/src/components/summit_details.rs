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

#[function_component(SummitDetails)]
pub fn component(props: &Props) -> Html {
    match use_context::<Vec<Summit>>()
        .expect("no ctx")
        .iter()
        .find(|x| x.reference == props.reference)
    {
        Some(summit) => html! {
            <article>
                <h3>
                    <Link<Route> to={Route::Summit{reference:summit.reference.clone()}}>{summit.reference.full()}</Link<Route>>
                    {", "}
                    {summit.name.clone()}
                    {" – "}
                    {format!("{:0.0}m",summit.alt)}
                </h3>
                <nav>
                    <a style="margin:0 .5em" href={format!("https://www.sotadata.org.uk/summit/{}",summit.reference.full())}>{"sotadata.org.uk"}</a>
                    <a style="margin:0 .5em" href={format!("https://sotl.as/summits/{}",summit.reference.full())}>{"sotl.as"}</a>
                </nav>
                <img src={format!("https://github.com/majkrzak/sp-sota-maps/releases/download/0.0.0/{}.png",summit.reference.slug())}/>
                <section>
                    <h4>{"Downloads"}</h4>
                    <nav>
                        <a class="button" style="margin:0 .5em" href={format!("https://github.com/majkrzak/sp-sota-maps/releases/download/0.0.0/{}.pdf",summit.reference.slug())}>{"A5 PDF"}</a>
                        <a class="button" style="margin:0 .5em" href={format!("https://github.com/majkrzak/sp-sota-maps/releases/download/0.0.0/{}.png",summit.reference.slug())}>{"1440p PNG"}</a>
                    </nav>
                </section>
            </article>
        },
        None => html! {{"todo"}},
    }
}
