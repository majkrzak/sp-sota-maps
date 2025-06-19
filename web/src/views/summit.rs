use yew::{html, Html};
use yew_router::prelude::Link;

use crate::{
    model::{release::Release, summit::Summit},
    router::Route,
};

pub fn summit_brief(summit: &Summit) -> Html {
    html! {
        <>
            <Link<Route> to={Route::Summit{reference:summit.reference.clone()}}>
                { summit.reference.full() }
            </Link<Route>>
            { ", " }
            { summit.name.clone() }
            { " – " }
            { format!("{:0.0}m",summit.alt) }
        </>
    }
}

pub fn summit_links(summit: &Summit) -> Html {
    html! {
        <>
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
        </>
    }
}

pub fn summit_image(release: &Release, summit: &Summit) -> Html {
    html! {
        <img
            src={release.asset(format!("{}.avif",summit.reference.slug()).as_str()).unwrap().browser_download_url.clone()}
        />
    }
}

pub fn summit_downloads(release: &Release, summit: &Summit) -> Html {
    html! {
        <>
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
        </>
    }
}
