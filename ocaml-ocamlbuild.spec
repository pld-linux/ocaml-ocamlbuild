#
# Conditional build:
%bcond_without	ocaml_opt	# skip building native optimized binaries (bytecode is always built)

# not yet available on x32 (ocaml 4.02.1), update when upstream will support it
%ifnarch %{ix86} %{x8664} arm aarch64 ppc sparc sparcv9
%undefine	with_ocaml_opt
%endif

%define		module	ocamlbuild
Summary:	Build tool for OCaml libraries and programs
Name:		ocaml-%{module}
Version:	0.11.0
Release:	1
License:	LGPLv2+ with exceptions
Group:		Development/Languages
Source0:	https://github.com/ocaml/ocamlbuild/archive/%{version}/%{module}-%{version}.tar.gz
# Source0-md5:	e3b83c842f82ef909b6d2a2d2035f0fe
URL:		https://github.com/ocaml/ocamlbuild
BuildRequires:	ocaml >= 1:4.04.0
%requires_eq	ocaml-runtime
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
OCamlbuild is a build tool for building OCaml libraries and programs.

%package devel
Summary:	Development files for %{module}
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
This package contains development files for %{module}.

%prep
%setup -q -n %{module}-%{version}

%build
%{__make} configure \
  OCAMLBUILD_PREFIX=%{_prefix} \
  OCAMLBUILD_BINDIR=%{_bindir} \
  OCAMLBUILD_LIBDIR=%{_libdir}/ocaml \
%ifarch %{ocaml_opt}
  OCAML_NATIVE=true
%else
  OCAML_NATIVE=false
%endif

%{__make}

%install
rm -rf $RPM_BUILD_ROOT
%{__make} install \
     DESTDIR=$RPM_BUILD_ROOT \
     CHECK_IF_PREINSTALLED=false

# Install the man page, which for some reason is not copied
# in by the make install rule above.
install -d $RPM_BUILD_ROOT%{_mandir}/man1/
install -p man/ocamlbuild.1 $RPM_BUILD_ROOT%{_mandir}/man1/

# move to dir pld ocamlfind looks
install -d $RPM_BUILD_ROOT%{_libdir}/ocaml/site-lib/%{module}
mv $OCAMLFIND_DESTDIR/%{module}/META \
	$RPM_BUILD_ROOT%{_libdir}/ocaml/site-lib/%{module}
cat <<EOF >> $RPM_BUILD_ROOT%{_libdir}/ocaml/site-lib/%{module}/META
directory="+%{module}"
EOF

%clean
rm -rf $RPM_BUILD_ROOT

%files
%defattr(644,root,root,755)
%doc Changes Readme.md VERSION
%attr(755,root,root) %{_bindir}/ocamlbuild
%attr(755,root,root) %{_bindir}/ocamlbuild.byte
%ifarch %{ocaml_opt}
%attr(755,root,root) %{_bindir}/ocamlbuild.native
%endif
%{_mandir}/man1/ocamlbuild.1*
%{_libdir}/ocaml/ocamlbuild
%ifarch %{ocaml_opt}
%exclude %{_libdir}/ocaml/ocamlbuild/*.a
%exclude %{_libdir}/ocaml/ocamlbuild/*.o
%exclude %{_libdir}/ocaml/ocamlbuild/*.cmx
%exclude %{_libdir}/ocaml/ocamlbuild/*.cmxa
%endif
%exclude %{_libdir}/ocaml/ocamlbuild/*.mli

%files devel
%defattr(644,root,root,755)
%doc manual/*
%ifarch %{ocaml_opt}
%{_libdir}/ocaml/ocamlbuild/*.a
%{_libdir}/ocaml/ocamlbuild/*.o
%{_libdir}/ocaml/ocamlbuild/*.cmx
%{_libdir}/ocaml/ocamlbuild/*.cmxa
%endif
%{_libdir}/ocaml/ocamlbuild/*.mli
