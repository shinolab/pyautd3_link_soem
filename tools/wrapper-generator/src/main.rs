mod parse;
mod python;
mod types;

use std::env;
use std::path::Path;

use anyhow::Result;

use cargo_metadata::MetadataCommand;
use parse::*;
use python::PythonGenerator;

pub fn gen<P1: AsRef<Path>, P2: AsRef<Path>>(crate_path: P1, dest_dir: P2) -> Result<()> {
    std::fs::create_dir_all(dest_dir.as_ref())?;

    let metadata = MetadataCommand::new()
        .manifest_path(crate_path.as_ref().join("Cargo.toml"))
        .exec()?;

    let crate_name = metadata.root_package().unwrap().name.as_str();

    glob::glob(&format!(
        "{}/**/*.rs",
        crate_path.as_ref().join("src").display()
    ))?
    .try_fold(PythonGenerator::new(), |acc, path| -> Result<_> {
        let path = path?;
        Ok(acc
            .register_enum(parse_enum(&path)?)
            .register_struct(parse_struct(&path)?, false))
    })?
    .write(dest_dir, crate_name, false)
}

pub fn gen_capi<P1: AsRef<Path>, P2: AsRef<Path>>(crate_path: P1, dest_dir: P2) -> Result<()> {
    std::fs::create_dir_all(dest_dir.as_ref())?;

    let metadata = MetadataCommand::new()
        .manifest_path(crate_path.as_ref().join("Cargo.toml"))
        .exec()?;

    let crate_name = metadata.root_package().unwrap().name.as_str();

    glob::glob(&format!(
        "{}/**/*.rs",
        crate_path.as_ref().join("src").display()
    ))?
    .try_fold(PythonGenerator::new(), |acc, path| -> Result<_> {
        let path = path?;
        Ok(acc
            .register_func(parse_func(&path)?)
            .register_const(parse_const(&path)?)
            .register_enum(parse_enum(&path)?)
            .register_union(parse_union(&path)?)
            .register_struct(parse_struct(&path)?, true))
    })?
    .write(dest_dir, crate_name, true)
}

fn main() -> Result<()> {
    let home = env::var("CARGO_MANIFEST_DIR")?;
    let home = Path::new(&home);
    {
        let crate_path = home
            .join("autd3-link-soem/Cargo.toml")
            .parent()
            .unwrap()
            .to_owned();
        gen(&crate_path, "../../pyautd3_link_soem/native_methods")?;
    }
    {
        let crate_path = home
            .join("autd3-capi-link-soem/Cargo.toml")
            .parent()
            .unwrap()
            .to_owned();
        gen_capi(&crate_path, "../../pyautd3_link_soem/native_methods")?;
    }

    Ok(())
}
