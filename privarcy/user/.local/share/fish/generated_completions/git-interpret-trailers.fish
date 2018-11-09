# git-interpret-trailers
# Autogenerated from man page /usr/share/man/man1/git-interpret-trailers.1.gz
complete -c git-interpret-trailers -l in-place --description 'Edit the files in place.'
complete -c git-interpret-trailers -l trim-empty --description 'If the <value> part of any trailer contains only whitespace, the whole traile…'
complete -c git-interpret-trailers -l trailer --description 'Specify a (<token>, <value>) pair that should be applied as a trailer to the …'
complete -c git-interpret-trailers -l where -l no-where --description 'Specify where all new trailers will be added.'
complete -c git-interpret-trailers -l if-exists -l no-if-exists --description 'Specify what action will be performed when there is already at least one trai…'
complete -c git-interpret-trailers -l if-missing -l no-if-missing --description 'Specify what action will be performed when there is no other trailer with the…'
complete -c git-interpret-trailers -l only-trailers --description 'Output only the trailers, not any other parts of the input.'
complete -c git-interpret-trailers -l only-input --description 'Output only trailers that exist in the input; do not add any from the command…'
complete -c git-interpret-trailers -l unfold --description 'Remove any whitespace-continuation in trailers, so that each trailer appears …'
complete -c git-interpret-trailers -l parse --description 'A convenience alias for --only-trailers --only-input --unfold.'

