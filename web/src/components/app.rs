use yew::{function_component, html, Html, Suspense};
use yew_router::{prelude::Link, HashRouter, Switch};

use crate::{
    components::{release_context::ReleaseContext, summits_context::SummitsContext},
    router::{render, Route},
    views::loading::loading,
};

#[function_component(App)]
pub fn component() -> Html {
    html! {
        <>
            <HashRouter>
                <header>
                    <nav>
                        <Link<Route> to={Route::Summits}>
                            <h1>{ "SP SOTA MAPS" }</h1>
                        </Link<Route>>
                    </nav>
                </header>
                <main>
                    <Suspense fallback={loading()}>
                        <ReleaseContext>
                            <SummitsContext>
                                <Switch<Route> {render} />
                            </SummitsContext>
                        </ReleaseContext>
                    </Suspense>
                </main>
                <footer>
                    <p>
                        { "SP-SOTA-MAPS © 2025 Piotr Majkrzak" }
                        <br />
                        <a href="https://github.com/majkrzak/sp-sota-maps">
                            { "github.com/majkrzak/sp-sota-maps" }
                        </a>
                    </p>
                </footer>
            </HashRouter>
        </>
    }
}
