{ self, ... }:
{
  _module.args.version =
    "${builtins.readFile ../version}+"
    + (
      if (self ? shortRev) then
        self.shortRev
      else if (self ? dirtyShortRev) then
        self.dirtyShortRev
      else
        "untracked"
    );
}
