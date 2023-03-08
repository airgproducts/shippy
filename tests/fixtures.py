import pytest

from shippy.base.schemas import Address


@pytest.fixture
def austrian_address_1():
    return Address(
        name="Hans Peter",
        address1="Wiesenweg 1",
        address2="Top 010",
        address3="Tuer 004",
        contactName="Hans Peter",
        zipcode="6020",
        city="Innsbruck",
        province="Tirol",
        countryCode="AT",
        email="hans.peter@foobar.com",
        phone="0123456789",
    )


@pytest.fixture
def austrian_address_2():
    return Address(
        name="Franz Richard",
        address1="Waldweg 3",
        address2="Top 2",
        address3="Tuer 1",
        contactName="Franz Richard",
        zipcode="1150",
        city="Wien",
        province="Wien",
        countryCode="AT",
        email="franz.richie@foobar.com",
        phone="0123456789",
    )


@pytest.fixture
def german_address_1():
    return Address(
        name="Anna Schmidt",
        address1="Blumenweg 3",
        address2="Top 20",
        address3="Tuer 11",
        contactName="Anna Schmidt",
        zipcode="10439",
        city="Berlin",
        province="Berlin",
        countryCode="DE",
        email="anna.schmidt@foobar.com",
        phone="0123456789",
    )


@pytest.fixture
def swiss_address_1():
    return Address(
        name="Lisa Meier",
        address1="Flussweg 3",
        address2="Top 77",
        address3="Tuer 5",
        contactName="Lisa Meier",
        zipcode="3001",
        city="Bern",
        province="Bern",
        countryCode="CH",
        email="lisa.meier@foobar.com",
        phone="0123456789",
    )
