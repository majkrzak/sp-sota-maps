use yew::Html;

use crate::views::error::error;

pub fn catch(f: impl FnOnce() -> anyhow::Result<Html>) -> Html {
    match f() {
        Ok(r) => r,
        Err(ref e) => {
            log::error!("{e:?}");
            error(e)
        }
    }
}
