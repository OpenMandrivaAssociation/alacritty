#!/usr/bin/bash

if [ ! $(which cargo-vendor) ]; then
	echo
	echo "cargo-vendor not found!"
	echo "You need to install the cargo-vendor package before running this script."
	exit
fi

VERSION=$(grep Version ../SPECS/alacritty.spec | cut -d: -f2 | sed -e 's|^[[:space:]]*||')
NAME=$(grep Name ../SPECS/alacritty.spec | cut -d: -f2 | sed -e 's|^[[:space:]]*||')

if [ ! -f ${NAME}-${VERSION}.tar.gz ]; then
	wget -q https://github.com/jwilm/alacritty/archive/v${VERSION}/${NAME}-${VERSION}.tar.gz
fi

tar xfz ${NAME}-${VERSION}.tar.gz
cd ${NAME}-${VERSION}
echo "Running cargo vendor for ${NAME}"
cargo vendor 3>&1 1> ../cargo-vendor.log 2>&1
tar cf ../${NAME}-cargo-vendor-${VERSION}.tar vendor
cd ..
echo "Compressing the ${NAME}-${VERSION} archive"
xz -e9 ${NAME}-cargo-vendor-${VERSION}.tar
rm -rf ${NAME}-${VERSION}
echo "Done"
