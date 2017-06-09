#
# Conditional build:
%bcond_without	ocaml_opt	# skip building native optimized binaries (bytecode is always built)

# not yet available on x32 (ocaml 4.02.1), update when upstream will support it
%ifnarch %{ix86} %{x8664} arm aarch64 ppc sparc sparcv9
%undefine	with_ocaml_opt
%endif

%define		module	ocamlbuild
Summary:	Build tool for OCaml libraries and programs
Summary(pl.UTF-8):	Narzędzie do budowania bibliotek i programów napisanych w OCamlu
Name:		ocaml-%{module}
Version:	0.11.0
Release:	2
License:	LGPL v2+ with exceptions
Group:		Development/Languages
Source0:	https://github.com/ocaml/ocamlbuild/archive/%{version}/%{module}-%{version}.tar.gz
# Source0-md5:	e3b83c842f82ef909b6d2a2d2035f0fe
Patch0:		%{name}-symlink.patch
URL:		https://github.com/ocaml/ocamlbuild
BuildRequires:	ocaml >= 1:4.04.0
%requires_eq	ocaml-runtime
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
OCamlbuild is a build tool for building OCaml libraries and programs.

%description -l pl.UTF-8
OCamlbuild to narzędzie do budowania bibliotek i programów napisanych
w OCamlu.

%package devel
Summary:	Development files for OCamlbuild library
Summary(pl.UTF-8):	Pliki programistyczne biblioteki OCamlbuild
Group:		Development/Libraries
Requires:	%{name} = %{version}-%{release}

%description devel
This package contains development files for OCamlbuild library.

%description devel -l pl.UTF-8
Ten pakiet zawiera pliki programistyczne biblioteki OCamlbuild.

%prep
%setup -q -n %{module}-%{version}
%patch0 -p1

%build
%{__make} configure \
	OCAMLBUILD_PREFIX=%{_prefix} \
	OCAMLBUILD_BINDIR=%{_bindir} \
	OCAMLBUILD_LIBDIR=%{_libdir}/ocaml \
	OCAML_NATIVE=%{?with_ocaml_opt:true}%{!?with_ocaml_opt:false}

%{__make}

%install
rm -rf $RPM_BUILD_ROOT

%{__make} install \
	DESTDIR=$RPM_BUILD_ROOT \
	CHECK_IF_PREINSTALLED=false

# Install the man page, which for some reason is not copied
# in by the make install rule above.
install -d $RPM_BUILD_ROOT%{_mandir}/man1
install -p man/ocamlbuild.1 $RPM_BUILD_ROOT%{_mandir}/man1

# move to dir pld ocamlfind looks
install -d $RPM_BUILD_ROOT%{_libdir}/ocaml/site-lib/%{module}
export OCAMLFIND_DESTDIR=$RPM_BUILD_ROOT%{_libdir}/ocaml
%{__mv} $OCAMLFIND_DESTDIR/%{module}/META \
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
%if %{with ocaml_opt}
%attr(755,root,root) %{_bindir}/ocamlbuild.native
%endif
%{_mandir}/man1/ocamlbuild.1*
%dir %{_libdir}/ocaml/ocamlbuild
%{_libdir}/ocaml/ocamlbuild/ocamlbuild*.cmi
%{_libdir}/ocaml/ocamlbuild/ocamlbuild.cmo
%{_libdir}/ocaml/ocamlbuild/ocamlbuildlib.cma

%files devel
%defattr(644,root,root,755)
%doc manual/*
%if %{with ocaml_opt}
%{_libdir}/ocaml/ocamlbuild/ocamlbuild*.o
%{_libdir}/ocaml/ocamlbuild/ocamlbuild*.cmx
%{_libdir}/ocaml/ocamlbuild/ocamlbuildlib.a
%{_libdir}/ocaml/ocamlbuild/ocamlbuildlib.cmxa
%endif
%{_libdir}/ocaml/ocamlbuild/signatures.mli
%{_libdir}/ocaml/site-lib/ocamlbuild
