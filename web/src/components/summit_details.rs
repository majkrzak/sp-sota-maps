use yew::{function_component, html, use_context, Html, Properties};
use yew_router::prelude::Link;

use crate::{
    model::{reference::Reference, release::Release, summit::Summit},
    router::Route,
};

#[derive(Properties, PartialEq, Clone)]
pub struct Props {
    pub reference: Reference,
}

#[function_component(SummitDetails)]
pub fn component(props: &Props) -> Html {
    let summits = use_context::<Vec<Summit>>().unwrap();
    let release = use_context::<Release>().unwrap();

    match summits.iter().find(|x| x.reference == props.reference) {
        Some(summit) => html! {
            <article>
                <h3>
                    <Link<Route> to={Route::Summit{reference:summit.reference.clone()}}>
                        { summit.reference.full() }
                    </Link<Route>>
                    { ", " }
                    { summit.name.clone() }
                    { " – " }
                    { format!("{:0.0}m",summit.alt) }
                </h3>
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
                <section>
                    <h4>{ "Insights" }</h4>
                    { {
                        let percentage = summit.insights.polish_area / summit.insights.total_area * 100.0;
                        if  percentage > 50.0 && summit.reference.association == "SP" {
                            html!{
                                <p>{format!("✔️ Over 50% ({percentage:.2}%) of the activation zone area is in Poland and summits belongs to SP.")}</p>
                            }
                        }
                        else if percentage < 50.0 && summit.reference.association != "SP" {
                            html!{
                                <p>{format!("✔️ Less than 50% ({percentage:.2}%) of the activation zone area is in Poland and summits does not belong to SP.")}</p>
                            }
                        }
                        else if  percentage > 50.0 && summit.reference.association != "SP" {
                            html!{
                                <p>{format!("❌ Over 50% ({percentage:.2}%) of the activation zone area is in Poland but summit does not belong to SP!")}</p>
                            }
                        }
                        else if percentage < 50.0 && summit.reference.association == "SP" {
                            html!{
                                <p>{format!("❌ Less than 50% ({percentage:.2}%) of the activation zone area is in Poland but summit belongs to SP!")}</p>
                            }
                        }
                        else {
                            html! {<p> {"Error"} </p>}
                        }
                    } }
                    { {
                        let tolarance = 1.0;
                        if summit.insights.elevation > tolarance {
                            html! {
                                <p>{format!("❌ Calculated peak altitude is greater than catalog one by ")} <mark> {format!{"{} m",summit.insights.elevation}} </mark> {"."} </p>
                            }
                        }
                        else if summit.insights.elevation < -tolarance {
                            html! {
                                <p>{format!("❌ Calculated peak altitude is lower than catalog one by ")} <mark> {format!{"{} m",-summit.insights.elevation}} </mark> {"."} </p>
                            }
                        }
                        else {
                            html! {
                                <p>{format!("✔️ Calculated peak altitude is OK.")} </p>
                            }
                        }
                    } }
                    { {
                        let tolarance = 10.0;
                        if summit.insights.distance > tolarance {
                            html! {
                                <p>{format!("❌ Calculated peak position differs from catalog one by ")} <mark> {format!{"{} m",summit.insights.distance}} </mark> {"."} </p>
                            }
                        }
                        else {
                            html! {
                                <p>{format!("✔️ Calculated peak position is OK.")} </p>
                            }
                        }
                    } }
                </section>
            </article>
        },
        None => html! { { "todo" } },
    }
}
