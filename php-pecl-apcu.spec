#
# Conditional build:
%bcond_without	web		# make web package

# don't build for php53
%if 0%{?_pld_builder:1} && "%{?php_suffix}" != "55"
%undefine	with_web
%endif

%define		php_name	php%{?php_suffix}
%define		modname	apcu
Summary:	APCu - APC User Cache
Name:		%{php_name}-pecl-%{modname}
Version:	4.0.11
Release:	1
License:	PHP 3.01
Group:		Development/Languages/PHP
Source0:	http://pecl.php.net/get/%{modname}-%{version}.tgz
# Source0-md5:	13c0c0dd676e5a7905d54fa985d0ee62
Source1:	%{modname}.ini
Source2:	apache.conf
Source3:	config.php
Patch0:		config.patch
URL:		http://pecl.php.net/package/APCu/
BuildRequires:	%{php_name}-devel >= 4:5.1.0
BuildRequires:	libtool
BuildRequires:	rpmbuild(macros) >= 1.666
%{?requires_php_extension}
Provides:	php(apcu) = %{version}
Obsoletes:	php-pecl-apcu < 4.0.4-2
BuildRoot:	%{tmpdir}/%{name}-%{version}-root-%(id -u -n)

%define		_webapps	/etc/webapps
%define		_webapp		%{modname}
%define		_sysconfdir	%{_webapps}/%{_webapp}
%define		_appdir		%{_datadir}/%{_webapp}

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

%package -n apcu-panel
Summary:	APCu control panel
Group:		Applications/Networking
Requires:	php(apcu) = %{version}
Requires:	php(gd)
Requires:	webapps
Requires:	webserver(access)
Requires:	webserver(php) >= 5.0
%if "%{_rpmversion}" >= "5"
BuildArch:	noarch
%endif

%description -n apcu-panel
This package provides the APCu control panel, with Webserver
configuration, available on <http://localhost/apcu-panel/>

%prep
%setup -qc
mv %{modname}-%{version}/* .
%patch0 -p1
cp -p %{SOURCE1} .

%build
%{__libtoolize}
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

# Install the Control Panel
%if %{with web}
install -d $RPM_BUILD_ROOT{%{_appdir},%{_sysconfdir}}
cp -p apc.php  $RPM_BUILD_ROOT%{_appdir}/index.php
cp -p %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/apache.conf
cp -p %{SOURCE2} $RPM_BUILD_ROOT%{_sysconfdir}/httpd.conf
cp -p %{SOURCE3} $RPM_BUILD_ROOT%{_sysconfdir}/config.php
%endif

%clean
rm -rf $RPM_BUILD_ROOT

%post
%php_webserver_restart

%postun
if [ "$1" = 0 ]; then
	%php_webserver_restart
fi

%triggerin -n apcu-panel -- apache1 < 1.3.37-3, apache1-base
%webapp_register apache %{_webapp}

%triggerun -n apcu-panel -- apache1 < 1.3.37-3, apache1-base
%webapp_unregister apache %{_webapp}

%triggerin -n apcu-panel -- apache < 2.2.0, apache-base
%webapp_register httpd %{_webapp}

%triggerun -n apcu-panel -- apache < 2.2.0, apache-base
%webapp_unregister httpd %{_webapp}

%files
%defattr(644,root,root,755)
%doc README.md NOTICE TECHNOTES.txt TODO INSTALL LICENSE
%config(noreplace) %verify(not md5 mtime size) %{php_sysconfdir}/conf.d/%{modname}.ini
%attr(755,root,root) %{php_extensiondir}/%{modname}.so

%if %{with web}
%files -n apcu-panel
%defattr(644,root,root,755)
%dir %attr(750,root,http) %{_sysconfdir}
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/apache.conf
%attr(640,root,root) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/httpd.conf
%attr(640,root,http) %config(noreplace) %verify(not md5 mtime size) %{_sysconfdir}/config.php
%{_appdir}
%endif
