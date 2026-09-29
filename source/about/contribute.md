# Contribute to nn

nn grows when people bring what they know. Find the role closest to yours below; every
contribution happens in the [NexusNoki](@@github_base@@) organisation on GitHub, and your name
is shown there with it.

nn is young and made by a small team. Parts of it are still rough, some platforms are thin, and
this manual has gaps; you will find them. That is where your help counts most. Reviews may take a
few days; every contribution is read.

## Everyday users: test this manual

**What.** Follow the manual on your own hardware, by yourself or with an AI assistant, and tell us
every step that is unclear, wrong or missing, or where you had to guess.

**How.** Open an issue on [nn-docs](@@github_base@@/nn-docs/issues) that names the page and the
step, what you expected, what happened, and the hardware you used. Photos of your setup are
welcome too.

## Software developers: fix and improve

**What.** Bug fixes, new features, tests and documentation for any part of nn.

**How.** For anything bigger than a small fix, open an issue first so the approach can be agreed.
Then send a pull request, with tests, against the **`nn/main/dev`** branch of the repository.
Accepted pull requests keep your name as their author.

## Embedded engineers: bring nn to new hardware

**What.** Support for a board, sensor or camera you think nn should run on, as a new `nn-app`
firmware.

**How.** Build it with the [nn-app-build](@@github_base@@/nn-app-build) SDK and follow the naming
of the existing apps. Like every nn device, it should be set up from the hub and take signed
over-the-air updates. Host it on your own GitHub, then open an issue asking for it to be forked
into NexusNoki; an accepted app is listed in this manual with your name.

## 3D printing experts: enclosures and mounts

**What.** Cases, mounts and covers for the boards nn runs on, indoors and out.

**How.** Share the source and printable files with print settings and photos of the printed part.
Accepted designs are linked from the matching pages of this manual.

## PCB designers: purpose-built boards

**What.** Boards made for nn: sensor boards, radio modules, camera carriers, or anything that makes
a device simpler, smaller or cheaper to build.

**How.** Publish the design files under **the licence you choose**: nn does not require one for
hardware. An embedded engineer can pair with you for the firmware.

## ISP tuning experts: better pictures

**What.** Colour, exposure and image-quality tuning for the image sensors nn cameras use.

**How.** Send the tuning files together with your method (test charts, light sources,
before-and-after pictures) as a pull request to the camera's repository.

## AI model experts: better detection

**What.** Detection models for the AI accelerators nn uses, better suited to home scenes, faster,
or more accurate.

**How.** Publish the model with a model card: the training data and its licence, the accuracy,
and the speed on the target hardware. nn loads its models from a replaceable model directory, so
a better model needs no code change.

## Chip designers and vendors: first-class support

**What.** Support for your chips and modules in nn: board support, AI runtimes, reference boards,
and help maintaining the port.

**How.** Write to the maintainers (see {ref}`contact`) to agree on the scope and on sample
hardware.

## OEMs and ODMs: build products on nn

**What.** Products that run nn. The Apache-2.0 licence allows commercial devices.

**How.** Keep the owner able to rebuild and reflash the firmware: that is nn's promise
({doc}`philosophy`). Name your product so it is not mistaken for the project itself, and write to
the maintainers (see {ref}`contact`) for integration help and to coordinate security fixes.

## For every contribution

- **Sign off your commits.** nn uses the [Developer Certificate of Origin](https://developercertificate.org/):
  every commit carries a `Signed-off-by:` line with your name and email, which states you have the
  right to contribute it. `git commit -s` adds it for you.
- **Licences.** Code contributions are under the repository's licence (Apache-2.0; this manual:
  CC-BY-4.0). Hardware designs keep the licence their authors choose.
- **Be kind.** Assume good intent, keep discussions about the work, and help newcomers.

(contact)=
## Contact

For vendors, OEMs and anything that should not be public, write to the maintainers by email.
**Security problems** go there too, never into a public issue.

```{todo}
Add the maintainers' email address (on the nexnok.com domain) once it exists, and open the public
nn/main/dev branches that pull requests go to.
```
