from dbus_next import BusType
from dbus_next.aio import MessageBus


async def new_rpm_ostree_interface():
    bus = await MessageBus(bus_type=BusType.SYSTEM).connect()
    sysroot_introspection = await bus.introspect(
        "org.projectatomic.rpmostree1", "/org/projectatomic/rpmostree1/Sysroot"
    )

    sysroot_proxy = bus.get_proxy_object(
        "org.projectatomic.rpmostree1",
        "/org/projectatomic/rpmostree1/Sysroot",
        sysroot_introspection,
    )
    sysroot = sysroot_proxy.get_interface("org.projectatomic.rpmostree1.Sysroot")

    booted_path = await sysroot.get_booted()

    booted_introspection = await bus.introspect(
        "org.projectatomic.rpmostree1", booted_path
    )

    booted_proxy = bus.get_proxy_object(
        "org.projectatomic.rpmostree1",
        booted_path,
        booted_introspection,
    )

    booted = booted_proxy.get_interface("org.projectatomic.rpmostree1.OS")

    booted_experimental = booted_proxy.get_interface(
        "org.projectatomic.rpmostree1.OS.Experimental"
    )

    return booted, booted_experimental
