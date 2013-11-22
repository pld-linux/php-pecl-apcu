%define		php_name	php%{?php_suffix}
%define		modname	apcu
Summary:	APCu - APC User Cache
Name:		%{php_name}-pecl-%{modname}
Version:	4.0.2
Release:	2
License:	PHP 3.01
Group:		Development/Languages/PHP
Source0:	http://pecl.php.net/get/%{modname}-%{version}.tgz
# Source0-md5:	c8a5c246b787eec81847017823099884
Source1:	%{modname}.ini
URL:		http://pecl.php.net/package/APCu/
BuildRequires:	%{php_name}-devel >= 4:5.1.0
BuildRequires:	rpmbuild(macros) >= 1.666
%{?requires_php_extension}
Requires:	php(core) >= 5.1.0
Provides:	php(apcu) = %{version}
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%description
APCu is userland caching: APC stripped of opcode caching in
preparation for the deployment of Zend Optimizer+ as the primary
solution to opcode caching in future versions of PHP.

APCu only supports userland caching (and dumping) of variables,
providing an upgrade path for the future. When O+ takes over, many
will be tempted to use 3rd party solutions to userland caching,
possibly even distributed solutions; this would be a grave error. The
tried and tested APC codebase provides far superior support for local
storage of PHP variables.

%prep
%setup -qc
mv %{modname}-%{version}/* .
cp -p %{SOURCE1} .

%build
phpize
%configure \
	--%{!?debug:dis}%{?debug:en}able-apcu-debug \
	--enable-apcu-spinlocks \
	--enable-apcu-mmap
%{__make}

%install
rm -rf $RPM_BUILD_ROOT
install -d $RPM_BUILD_ROOT{%{php_extensiondir},%{php_sysconfdir}/conf.d}
install -p modules/apcu.so $RPM_BUILD_ROOT%{php_extensiondir}/%{modname}.so
cp -p %{modname}.ini $RPM_BUILD_ROOT%{php_sysconfdir}/conf.d/%{modname}.ini

%clean
rm -rf $RPM_BUILD_ROOT

%post
%php_webserver_restart

%postun
if [ "$1" = 0 ]; then
	%php_webserver_restart
fi

%files
%defattr(644,root,root,755)
%doc README.md NOTICE TECHNOTES.txt TODO INSTALL LICENSE
%config(noreplace) %verify(not md5 mtime size) %{php_sysconfdir}/conf.d/%{modname}.ini
%attr(755,root,root) %{php_extensiondir}/%{modname}.so
