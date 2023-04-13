
# Snapshot & Checkpoint

[incremental-backup](https://libvirt.org/kbase/internals/incremental-backup.html)

## Snapshot

Similarly to a checkpoint it's a point in time in the lifecycle of the VM but the state of the VM including memory is captured at that point allowing returning to the state later.

## Checkpoint

A libvirt object which represents a named point in time of the life of the vm where libvirt tracks writes the VM has done, thereby allowing a backup of only the blocks which changed. Note that state of the VM memory is _not_ captured.
