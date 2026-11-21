#!/bin/sh
set -e
BASE_DIR=$(CDPATH= cd -- "$(dirname -- "$0")" && pwd)
VERSION=3.9.11
HOME_DIR="${MAVEN_USER_HOME:-$HOME/.m2}/wrapper/dists/apache-maven-$VERSION"
MAVEN="$HOME_DIR/apache-maven-$VERSION/bin/mvn"
URL="https://repo.maven.apache.org/maven2/org/apache/maven/apache-maven/$VERSION/apache-maven-$VERSION-bin.zip"
if [ ! -x "$MAVEN" ]; then
  mkdir -p "$HOME_DIR"
  ZIP="$HOME_DIR/maven.zip"
  if command -v curl >/dev/null 2>&1; then curl -fsSL "$URL" -o "$ZIP"; else wget -q "$URL" -O "$ZIP"; fi
  unzip -q -o "$ZIP" -d "$HOME_DIR"
  rm -f "$ZIP"
fi
exec "$MAVEN" -f "$BASE_DIR/pom.xml" "$@"
