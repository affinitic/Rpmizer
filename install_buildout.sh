#!/bin/bash
set -e

if [ $# -lt 3 ]; then
    echo "Install buildout awaits buildout_dir, target_dir and rpm_build_root passed as arguments"
fi

BUILDOUT_DIR=$1
TARGET_DIR=$2
RPM_BUILD_ROOT=$3

# workaround buildout 2.2 bug where buildout does not install its own egg
# in buildout:directory/eggs
fix_buildout_22() {
    set +e
    grep "base = os.path.dirname(base)" "$@"
    if [ "$?" -eq "0" ]; then
        sed -i "s:^ *'[^ ]*\(eggs/zc.buildout.*egg\)',$:  join(base, '\1'),:g" "$@"
    else
        sed -i "s:^ *'[^ ]*\(eggs/zc.buildout.*egg\)',$:  '$TARGET_DIR/\1',:g" "$@"
    fi
    set -e
}

INSTALL_DIR=$RPM_BUILD_ROOT$TARGET_DIR
mkdir -p "$INSTALL_DIR/etc"
mv "$BUILDOUT_DIR/bin" "$BUILDOUT_DIR/var" "$BUILDOUT_DIR/parts" "$BUILDOUT_DIR/eggs" "$INSTALL_DIR"
for file in $INSTALL_DIR/bin/*
do
    sed -i "s:${BUILDOUT_DIR/:/\\:}:${TARGET_DIR/:/\\:}:g" "$file"
    fix_buildout_22 "$file"
done
cd "$INSTALL_DIR/"
rm -fr "$INSTALL_DIR/parts/docs"
rm -fr "$INSTALL_DIR/.git"
rm "$INSTALL_DIR/bin/instance"
rm -f "$INSTALL_DIR"/bin/pil*.py
rm "$INSTALL_DIR/bin/copy_ckeditor_code"
rm -rf "$INSTALL_DIR/parts/instance"
rm -rf "$INSTALL_DIR/parts/lxml"
find "$INSTALL_DIR" -name "*.pyc" -delete;
find "$INSTALL_DIR" -name "*.pyo" -delete;
for file in $INSTALL_DIR/parts/zeoserver/bin/*
do
    sed -i "s:${BUILDOUT_DIR/:/\\:}:${TARGET_DIR/:/\\:}:g" "$file"
    fix_buildout_22 "$file"
done
TO_CLEAN_UP=( \
    zeoserver/etc/zeo.conf \
    client1/etc/zope.conf \
    client2/etc/zope.conf \
    client3/etc/zope.conf \
    client4/etc/zope.conf \
    client1/bin/interpreter \
    client2/bin/interpreter \
    client3/bin/interpreter \
    client4/bin/interpreter \
)
for file in "${TO_CLEAN_UP[@]}"
do
    sed -i "s:${BUILDOUT_DIR/:/\\:}:${TARGET_DIR/:/\\:}:g" "$INSTALL_DIR/parts/$file"
    fix_buildout_22 "$INSTALL_DIR/parts/$file"
done
