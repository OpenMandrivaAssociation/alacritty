Name:           alacritty
Version:	0.12.2
Release:	1
Summary:        A cross-platform, GPU-accelerated terminal emulator
Group:          Terminals
License:        ASL 2.0
URL:            https://github.com/jwilm/alacritty
Source0:        https://github.com/jwilm/alacritty/archive/v%{version}/%{name}-%{version}.tar.gz
Source4:	https://github.com/jwilm/alacritty/releases/download/v%{version}/Alacritty.svg

# This is the script that creates the Source1 tar-ball needed to build without net access.
# Update the version here and then run the script.
# You need to have the "vendor" package for cargo installed.
# To install: urpmi cargo-vendor
Source100:      pack-cargo-vendor.sh

BuildRequires:  cargo
BuildRequires:  freetype-devel
BuildRequires:  pkgconfig(fontconfig)
BuildRequires:  pkgconfig(xcb)
BuildRequires:  desktop-file-utils
BuildRequires:  pkgconfig(xkbcommon)
BuildRequires:  pkgconfig(xkbcommon-x11)

Requires(post): ncurses
Requires(post): ncurses-extraterms
Recommends:     xclip

Recommends:     tmux

%description
Alacritty is focused on simplicity and performance. The performance goal means
it should be faster than any other terminal emulator available. The simplicity
goal means that it doesn't have features such as tabs or splits (which can be
better provided by a window manager or terminal multiplexer) nor niceties
like a GUI config editor.

The software is considered to be at an alpha level of readiness - there are
missing features and bugs to be fixed, but it is already used by many as a
daily driver.

%package zsh-completion
Summary:        A cross-platform, GPU-accelerated terminal emulator
Group:          Terminals
BuildArch:      noarch
Requires:       zsh
Requires:       %{name} >= %{version}-%{release}

%description zsh-completion
This is the shell completion for ZSH.

%package bash-completion
Summary:        A cross-platform, GPU-accelerated terminal emulator
Group:          Terminals
BuildArch:      noarch
Requires:       bash
Requires:       %{name} >= %{version}-%{release}

%description bash-completion
This is the shell completion for BASH.

%package fish-completion
Summary:        A cross-platform, GPU-accelerated terminal emulator
Group:          Terminals
BuildArch:      noarch
Recommends:       fish
Requires:       %{name} >= %{version}-%{release}

%description fish-completion
This is the shell completion for FISH.

%package docs
Summary:        A cross-platform, GPU-accelerated terminal emulator
Group:          Terminals
BuildArch:      noarch
Requires:       %{name} >= %{version}-%{release}

%description docs
The documentation for %{name}.

%prep
%autosetup -p1 -n %{name}-%{version}

mv extra/linux/Alacritty.desktop extra/linux/%{name}.desktop

%build
cargo build --release --verbose
cargo doc --verbose

%install
%__mkdir_p %{buildroot}%{_bindir}
%__mkdir_p %{buildroot}%{_datadir}/applications
%__mkdir_p %{buildroot}%{_iconsdir}
%__mkdir_p %{buildroot}%{_datadir}/pixmaps
%__install -Dm 0755 extra/logo/*svg %{buildroot}%{_iconsdir}/
%__install -Dm 0755 %{S:4} %{buildroot}%{_datadir}/pixmaps/
%__install -Dm 0755 target/release/%{name} %{buildroot}%{_bindir}/%{name}
desktop-file-install extra/linux/%{name}.desktop \
  --dir %{buildroot}%{_datadir}/applications %{buildroot}%{_datadir}/applications/%{name}.desktop

# Shell completions
%__mkdir_p %{buildroot}%{_datadir}/zsh/site-functions/
%__mkdir_p %{buildroot}%{_datadir}/bash-completion/completions/
%__mkdir_p %{buildroot}%{_datadir}/fish/completions/
%__mkdir_p %{buildroot}%{_mandir}/man1
%__mkdir_p %{buildroot}%{_docdir}/%{name}
cp extra/completions/_%{name} %{buildroot}%{_datadir}/zsh/site-functions/_%{name}
cp extra/completions/%{name}.bash %{buildroot}%{_datadir}/bash-completion/completions/%{name}
cp extra/completions/%{name}.fish %{buildroot}%{_datadir}/fish/completions/%{name}.fish
%__install -Dm 0644 extra/%{name}.man %{buildroot}%{mandir}/man1/%{name}.1
%__install -Dm 0644 extra/%{name}.info %{buildroot}%{_docdir}/%{name}/%{name}.info

rm -vf %{buildroot}%{_prefix}/.crates.toml

%post
echo "        Adding %{name} info to terminfo"
tic -e alacritty,alacritty-direct %{_docdir}/%{name}/%{name}.info > /dev/null 2>&1

%files
%license LICENSE-APACHE
%doc README.md CONTRIBUTING.md
%{_bindir}/%{name}
%{_datadir}/applications/*.desktop
%{_datadir}/pixmaps/Alacritty.svg
%{_docdir}/%{name}/%{name}.info
%{_iconsdir}/%{name}*svg

%files bash-completion
%{_datadir}/bash-completion/completions/%{name}

%files fish-completion
%{_datadir}/fish/completions/%{name}.fish

%files zsh-completion
%{_datadir}/zsh/site-functions/_%{name}

%files docs
%doc target/doc/alacritty/
