use yew::{function_component, html, Html, Properties};

use crate::model::reference::Reference;

#[derive(Properties, PartialEq)]
pub struct Props {
    pub reference: Reference,
}

#[function_component(Summit)]
pub fn component(props: &Props) -> Html {
    html! {
        <article>
            <h3>{props.reference.full()}</h3>
            <nav>
                <a style="margin:0 .5em" href={format!("https://www.sotadata.org.uk/summit/{}",props.reference.full())}>{"sotadata.org.uk"}</a>
                <a style="margin:0 .5em" href={format!("https://sotl.as/summits/{}",props.reference.full())}>{"sotl.as"}</a>
            </nav>
            <img src={format!("https://github.com/majkrzak/sp-sota-maps/releases/download/0.0.0/{}.png",props.reference.slug())}/>
            <section>
                <h4>{"Downloads"}</h4>
                <nav>
                    <a class="button" style="margin:0 .5em" href={format!("https://github.com/majkrzak/sp-sota-maps/releases/download/0.0.0/{}.pdf",props.reference.slug())}>{"A5 PDF"}</a>
                    <a class="button" style="margin:0 .5em" href={format!("https://github.com/majkrzak/sp-sota-maps/releases/download/0.0.0/{}.png",props.reference.slug())}>{"1440p PNG"}</a>
                </nav>
            </section>
        </article>
    }
}
