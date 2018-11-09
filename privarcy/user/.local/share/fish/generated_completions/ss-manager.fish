# ss-manager
# Autogenerated from man page /usr/share/man/man1/ss-manager.1.gz
complete -c ss-manager -s s --description 'Set the server\\(cqs hostname or IP.'
complete -c ss-manager -s k --description 'Set the password.  The server and the client should use the same password.'
complete -c ss-manager -s m --description 'Set the cipher. sp Shadowsocks-libev accepts 18 different ciphers: .'
complete -c ss-manager -s a --description 'Run as a specific user.'
complete -c ss-manager -s f --description 'Start shadowsocks as a daemon with specific pid file.'
complete -c ss-manager -s t --description 'Set the socket timeout in seconds.  The default value is 60.'
complete -c ss-manager -s c --description 'Use a configuration file.'
complete -c ss-manager -s i --description 'Send traffic through specific network interface.'
complete -c ss-manager -s u --description 'Enable UDP relay.'
complete -c ss-manager -s U --description 'Enable UDP relay and disable TCP relay.'
complete -c ss-manager -s A --description 'Enable onetime authentication.'
complete -c ss-manager -s d --description 'Setup name servers for internal DNS resolver (libudns).'
complete -c ss-manager -l fast-open --description 'Enable TCP fast open. sp Only available with Linux kernel > 3. 7. 0.'
complete -c ss-manager -l reuse-port --description 'Enable port reuse. sp Only available with Linux kernel > 3. 9. 0.'
complete -c ss-manager -l acl --description 'Enable ACL (Access Control List) and specify config file.'
complete -c ss-manager -l manager-address --description 'Specify UNIX domain socket address for the communication between ss-manager(1…'
complete -c ss-manager -l executable --description 'Specify the executable path of ss-server. sp Only available in manager mode.'
complete -c ss-manager -l plugin --description 'Enable SIP003 plugin.  (Experimental).'
complete -c ss-manager -l plugin-opts --description 'Set SIP003 plugin options.  (Experimental).'
complete -c ss-manager -s v --description 'Enable verbose mode.'
complete -c ss-manager -s h -l help --description 'Print help message.'

