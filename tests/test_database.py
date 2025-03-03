from datetime import datetime, timezone
import unittest
from unittest.mock import patch, MagicMock
from sqlalchemy.exc import IntegrityError, SQLAlchemyError
from typing import List


import homestake.constants as const
from homestake.database.client import DatabaseClient, DatabaseClientError, DatabaseDuplicationError
from homestake.database.models import Account, Mortgage, Property, Transaction, User


class TestMortgage(unittest.TestCase):
    def setUp(self):
        self.db_client = DatabaseClient()

    def test_create_mortgage_required_args(self):
        mortgage_id = 1
        lender = "testlender"
        amount = 100000.00
        interest_rate = 5
        term = 30
        start_date = datetime.now(timezone.utc)
        with patch("homestake.database.client.Session") as mock_session:
            mock_session.return_value.__enter__.return_value.add = MagicMock(
                side_effect=lambda mortgage: setattr(mortgage, "id", mortgage_id) or setattr(mortgage, "start_date", start_date))
            mock_session.return_value.__enter__.return_value.commit = MagicMock()

            result = self.db_client.create_mortgage(
                lender, amount, interest_rate, term, start_date)
            self.assertEqual(result["id"], mortgage_id)
            self.assertEqual(result["loan_amount"], amount)
            self.assertEqual(result["interest_rate"], interest_rate)
            self.assertEqual(result["term"], term)

            mock_session.return_value.__enter__.return_value.add.assert_called_once()
            mock_session.return_value.__enter__.return_value.commit.assert_called_once()

    def test_create_mortgage_optional_args(self):
        mortgage_id = 1
        lender = "testlender"
        property_id = 2
        amount = 100000.00
        interest_rate = 5
        term = 30
        start_date = datetime.now(timezone.utc)
        with patch("homestake.database.client.Session") as mock_session:
            mock_session.return_value.__enter__.return_value.add = MagicMock(
                side_effect=lambda mortgage: setattr(mortgage, "id", mortgage_id) or setattr(mortgage, "start_date", start_date))
            mock_session.return_value.__enter__.return_value.commit = MagicMock()

            result = self.db_client.create_mortgage(
                lender, amount, interest_rate, term, start_date, property_id)
            self.assertEqual(result["id"], mortgage_id)
            self.assertEqual(result["loan_amount"], amount)
            self.assertEqual(result["interest_rate"], interest_rate)
            self.assertEqual(result["term"], term)

            mock_session.return_value.__enter__.return_value.add.assert_called_once()
            mock_session.return_value.__enter__.return_value.commit.assert_called_once()

    def test_create_mortgage_integrity_error_name_exists(self):
        lender = "testlender"
        amount = 100000.00
        interest_rate = 5
        term = 30
        start_date = datetime.now(timezone.utc)
        with patch("homestake.database.client.Session") as mock_session:
            mock_session.return_value.__enter__.return_value.add = MagicMock()
            mock_session.return_value.__enter__.return_value.commit.side_effect = IntegrityError(
                f"{const.DB_ENTRY_EXISTS_MSG}: mortgage.name", "mock", "mock")
            mock_session.return_value.__enter__.return_value.rollback = MagicMock()

            with self.assertRaisesRegex(DatabaseDuplicationError, const.MORTGAGE_EXISTS_MSG):
                self.db_client.create_mortgage(
                    lender, amount, interest_rate, term, start_date)

            mock_session.return_value.__enter__.return_value.rollback.assert_called_once()

    def test_create_mortgage_integrity_error_name_no_exists(self):
        lender = "testlender"
        amount = 100000.00
        interest_rate = 5
        term = 30
        start_date = datetime.now(timezone.utc)
        with patch("homestake.database.client.Session") as mock_session:
            mock_session.return_value.__enter__.return_value.add = MagicMock()
            mock_session.return_value.__enter__.return_value.commit.side_effect = IntegrityError(
                "mock", "mock", "mock")
            mock_session.return_value.__enter__.return_value.rollback = MagicMock()

            with self.assertRaisesRegex(DatabaseClientError, const.MORTGAGE_CREATE_ERROR_MSG):
                self.db_client.create_mortgage(
                    lender, amount, interest_rate, term, start_date)

            mock_session.return_value.__enter__.return_value.rollback.assert_called_once()

    def test_create_mortgage_sqlalchemy_error(self):
        lender = "testlender"
        amount = 100000.00
        interest_rate = 5
        term = 30
        start_date = datetime.now(timezone.utc)
        with patch("homestake.database.client.Session") as mock_session:
            mock_session.return_value.__enter__.return_value.add = MagicMock()
            mock_session.return_value.__enter__.return_value.commit.side_effect = SQLAlchemyError(
                "mock")
            mock_session.return_value.__enter__.return_value.rollback = MagicMock()

            with self.assertRaisesRegex(DatabaseClientError, const.MORTGAGE_CREATE_ERROR_MSG):
                self.db_client.create_mortgage(
                    lender, amount, interest_rate, term, start_date)

            mock_session.return_value.__enter__.return_value.rollback.assert_called_once()

    def test_get_mortgage_by_id(self):
        mortgage_id = 1
        lender = "testlender"
        amount = 100000.00
        interest_rate = 5
        term = 30
        start_date = datetime.now(timezone.utc)
        with patch("homestake.database.client.Session") as mock_session:
            mock_session.return_value.__enter__.return_value.query = MagicMock(
                return_value=MagicMock(
                    filter_by=MagicMock(
                        return_value=MagicMock(
                            first=MagicMock(return_value=Mortgage(
                                id=mortgage_id,
                                lender=lender,
                                loan_amount=amount,
                                interest_rate=interest_rate,
                                term=term,
                                start_date=start_date
                            ))
                        )
                    )
                )
            )

            result = self.db_client.get_mortgage_by_id(mortgage_id)
            self.assertEqual(result["id"], mortgage_id)
            self.assertEqual(result["lender"], lender)
            self.assertEqual(result["loan_amount"], amount)
            self.assertEqual(result["interest_rate"], interest_rate)
            self.assertEqual(result["term"], term)
            self.assertEqual(result["start_date"], start_date.isoformat())

            mock_session.return_value.__enter__.return_value.query.assert_called_once()

    def test_get_mortgage_by_lender(self):
        mortgage_id = 1
        lender = "testlender"
        amount = 100000.00
        interest_rate = 5
        term = 30
        start_date = datetime.now(timezone.utc)
        with patch("homestake.database.client.Session") as mock_session:
            mock_session.return_value.__enter__.return_value.query = MagicMock(
                return_value=MagicMock(
                    filter_by=MagicMock(
                        return_value=MagicMock(
                            first=MagicMock(return_value=Mortgage(
                                id=mortgage_id,
                                lender=lender,
                                loan_amount=amount,
                                interest_rate=interest_rate,
                                term=term,
                                start_date=start_date
                            ))
                        )
                    )
                )
            )

            result = self.db_client.get_mortgage_by_lender(lender)
            self.assertEqual(result["id"], mortgage_id)
            self.assertEqual(result["lender"], lender)
            self.assertEqual(result["loan_amount"], amount)
            self.assertEqual(result["interest_rate"], interest_rate)
            self.assertEqual(result["term"], term)
            self.assertEqual(result["start_date"], start_date.isoformat())

            mock_session.return_value.__enter__.return_value.query.assert_called_once()

    def test_get_mortgage_by_property(self):
        mortgage_id = 1
        lender = "testlender"
        amount = 100000.00
        interest_rate = 5
        term = 30
        start_date = datetime.now(timezone.utc)
        property_id = 2
        with patch("homestake.database.client.Session") as mock_session:
            mock_session.return_value.__enter__.return_value.query = MagicMock(
                return_value=MagicMock(
                    filter_by=MagicMock(
                        return_value=MagicMock(
                            first=MagicMock(return_value=Mortgage(
                                id=mortgage_id,
                                lender=lender,
                                loan_amount=amount,
                                interest_rate=interest_rate,
                                term=term,
                                start_date=start_date,
                                property_id=property_id
                            ))
                        )
                    )
                )
            )

            result = self.db_client.get_mortgage_by_property(property_id)
            self.assertEqual(result["id"], mortgage_id)
            self.assertEqual(result["lender"], lender)
            self.assertEqual(result["loan_amount"], amount)
            self.assertEqual(result["interest_rate"], interest_rate)
            self.assertEqual(result["term"], term)
            self.assertEqual(result["start_date"], start_date.isoformat())

            mock_session.return_value.__enter__.return_value.query.assert_called_once()

    def test_update_mortgage(self):
        old_lender = "testlender"
        new_lender = "newlender"
        mortgage_id = 1
        amount = 100000.00
        interest_rate = 5
        term = 30
        start_date = datetime.now(timezone.utc)
        with patch("homestake.database.client.Session") as mock_session:
            test_mortgage = Mortgage(
                id=mortgage_id, lender=old_lender, loan_amount=amount, interest_rate=interest_rate, term=term, start_date=start_date)

            mock_query = MagicMock()
            mock_session.return_value.__enter__.return_value.query.side_effect = [
                mock_query, mock_query]
            mock_query.filter_by.return_value.first.return_value = test_mortgage

            self.assertEqual(test_mortgage.lender, old_lender)
            result = self.db_client.update_mortgage(
                mortgage_id, lender=new_lender)
            self.assertEqual(result["id"], mortgage_id)
            self.assertEqual(result["lender"], new_lender)
            self.assertEqual(result["loan_amount"], amount)
            self.assertEqual(result["interest_rate"], interest_rate)
            self.assertEqual(result["term"], term)
            self.assertEqual(result["start_date"], start_date.isoformat())

            self.assertEqual(mock_query.filter_by.call_count, 1)
            mock_query.filter_by.assert_any_call(id=mortgage_id)
            mock_session.return_value.__enter__.return_value.commit.assert_called_once()

    def test_update_mortgage_sqlalchemy_error(self):
        old_lender = "testlender"
        new_lender = "newlender"
        mortgage_id = 1
        amount = 100000.00
        interest_rate = 5
        term = 30
        start_date = datetime.now(timezone.utc)
        with patch("homestake.database.client.Session") as mock_session:
            test_mortgage = Mortgage(
                lender=old_lender, loan_amount=amount, interest_rate=interest_rate, term=term, start_date=start_date)

            mock_query = MagicMock()
            mock_session.return_value.__enter__.return_value.query.side_effect = [
                mock_query, mock_query]
            mock_query.filter_by.return_value.first.return_value = test_mortgage
            mock_session.return_value.__enter__.return_value.commit.side_effect = SQLAlchemyError(
                "mock")

            with self.assertRaisesRegex(DatabaseClientError, const.MORTGAGE_UPDATE_ERROR_MSG):
                self.db_client.update_mortgage(
                    mortgage_id, lender=new_lender)

            self.assertEqual(mock_query.filter_by.call_count, 1)
            mock_query.filter_by.assert_any_call(id=mortgage_id)
            mock_session.return_value.__enter__.return_value.rollback.assert_called_once()

    def test_update_mortgage_not_found(self):
        new_lender = "newlender"
        mortgage_id = 1
        with patch("homestake.database.client.Session") as mock_session:
            mock_query = MagicMock()
            mock_session.return_value.__enter__.return_value.query.side_effect = [
                mock_query, mock_query]
            mock_query.filter_by.return_value.first.return_value = None

            with self.assertRaisesRegex(DatabaseClientError, const.MORTGAGE_ID_NOT_FOUND.format(mortgage_id)):
                self.db_client.update_mortgage(
                    mortgage_id, lender=new_lender)

            self.assertEqual(mock_query.filter_by.call_count, 1)
            mock_query.filter_by.assert_any_call(id=mortgage_id)
            mock_session.return_value.__enter__.return_value.commit.assert_not_called()
            mock_session.return_value.__enter__.return_value.rollback.assert_not_called()

    def test_delete_mortgage(self):
        mortgage_id = 1
        start_date = datetime.now(timezone.utc)
        with patch("homestake.database.client.Session") as mock_session:
            mock_session.return_value.__enter__.return_value.query.return_value.filter_by.return_value.first.return_value = Mortgage(
                id=mortgage_id,
                start_date=start_date
            )
            mock_session.return_value.__enter__.return_value.delete = MagicMock()

            result = self.db_client.delete_mortgage(mortgage_id)
            self.assertEqual(result["id"], mortgage_id)
            self.assertEqual(result["start_date"], start_date.isoformat())

            mock_session.return_value.__enter__.return_value.query.assert_called_once()
            mock_session.return_value.__enter__.return_value.query.return_value.filter_by.assert_called_once_with(
                id=mortgage_id)
            mock_session.return_value.__enter__.return_value.delete.assert_called_once()

    def test_delete_mortgage_sqlalchemy_error(self):
        mortgage_id = 1
        start_date = datetime.now(timezone.utc)
        with patch("homestake.database.client.Session") as mock_session:
            mock_session.return_value.__enter__.return_value.query.return_value.filter_by.return_value.first.return_value = Mortgage(
                start_date=start_date
            )
            mock_session.return_value.__enter__.return_value.delete.side_effect = SQLAlchemyError(
                "mock")
            mock_session.return_value.__enter__.return_value.rollback = MagicMock()

            with self.assertRaisesRegex(DatabaseClientError, const.MORTGAGE_DELETE_ERROR_MSG):
                self.db_client.delete_mortgage(mortgage_id)

            mock_session.return_value.__enter__.return_value.rollback.assert_called_once()

    def test_delete_mortgage_not_found(self):
        mortgage_id = 1
        with patch("homestake.database.client.Session") as mock_session:
            mock_session.return_value.__enter__.return_value.query.return_value.filter_by.return_value.first.return_value = None

            with self.assertRaisesRegex(DatabaseClientError, const.MORTGAGE_ID_NOT_FOUND.format(mortgage_id)):
                self.db_client.delete_mortgage(mortgage_id)

            mock_session.return_value.__enter__.return_value.query.return_value.filter_by.assert_called_once_with(
                id=mortgage_id)
            mock_session.return_value.__enter__.return_value.commit.assert_not_called()
            mock_session.return_value.__enter__.return_value.rollback.assert_not_called()

    def test_list_mortgages(self):
        mortgage_id = 1
        lender = "testlender"
        start_date = datetime.now(timezone.utc)
        with patch("homestake.database.client.Session") as mock_session:
            mock_query = MagicMock()
            mock_query.all.return_value = [
                Mortgage(id=mortgage_id, lender=lender, start_date=start_date)]
            mock_session.return_value.__enter__.return_value.query.return_value = mock_query

            mortgages = self.db_client.list_mortgages()
            self.assertTrue(isinstance(mortgages, List))
            self.assertTrue(all(mortgage["id"] == mortgage_id and mortgage["lender"]
                            == lender and mortgage["start_date"] == start_date.isoformat() for mortgage in mortgages))

            mock_session.return_value.__enter__.return_value.query.assert_called_once()
            mock_query.all.assert_called_once()


class TestProperty(unittest.TestCase):
    def setUp(self):
        self.db_client = DatabaseClient()

    def test_create_property(self):
        property_id = 1
        property_name = "primary residence"
        address = "123 Test St"
        purchase_price = 100000.00
        purchase_date = datetime.now(timezone.utc)
        current_value = 110000.00
        with patch("homestake.database.client.Session") as mock_session:
            mock_session.return_value.__enter__.return_value.add = MagicMock(
                side_effect=lambda property: setattr(property, "id", property_id))
            mock_session.return_value.__enter__.return_value.commit = MagicMock()

            property = self.db_client.create_property(
                property_name, address, purchase_price, purchase_date, current_value)
            self.assertEqual(property["id"], property_id)
            self.assertEqual(property["name"], property_name)
            self.assertEqual(property["address"], address)
            self.assertEqual(property["purchase_price"], purchase_price)
            self.assertEqual(property["purchase_date"],
                             purchase_date.isoformat())
            self.assertEqual(property["current_value"], current_value)

            mock_session.return_value.__enter__.return_value.add.assert_called_once()
            mock_session.return_value.__enter__.return_value.commit.assert_called_once()

    def test_create_property_integrity_error_name_exists(self):
        property_name = "primary residence"
        address = "123 Test St"
        purchase_price = 100000.00
        purchase_date = datetime.now(timezone.utc)
        current_value = 110000.00
        with patch("homestake.database.client.Session") as mock_session:
            mock_session.return_value.__enter__.return_value.add = MagicMock()
            mock_session.return_value.__enter__.return_value.commit.side_effect = IntegrityError(
                f"{const.DB_ENTRY_EXISTS_MSG}: properties.name", "mock", "mock")
            mock_session.return_value.__enter__.return_value.rollback = MagicMock()

            with self.assertRaisesRegex(DatabaseDuplicationError, const.PROPERTY_EXISTS_MSG):
                self.db_client.create_property(
                    property_name, address, purchase_price, purchase_date, current_value)

            mock_session.return_value.__enter__.return_value.rollback.assert_called_once()

    def test_create_property_integrity_error_name_address(self):
        property_name = "primary residence"
        address = "123 Test St"
        purchase_price = 100000.00
        purchase_date = datetime.now(timezone.utc)
        current_value = 110000.00
        with patch("homestake.database.client.Session") as mock_session:
            mock_session.return_value.__enter__.return_value.add = MagicMock()
            mock_session.return_value.__enter__.return_value.commit.side_effect = IntegrityError(
                f"{const.DB_ENTRY_EXISTS_MSG}: properties.address", "mock", "mock")
            mock_session.return_value.__enter__.return_value.rollback = MagicMock()

            with self.assertRaisesRegex(DatabaseDuplicationError, const.PROPERTY_EXISTS_MSG):
                self.db_client.create_property(
                    property_name, address, purchase_price, purchase_date, current_value)

            mock_session.return_value.__enter__.return_value.rollback.assert_called_once()

    def test_create_property_sqlalchemy_error(self):
        property_name = "primary residence"
        address = "123 Test St"
        purchase_price = 100000.00
        purchase_date = datetime.now(timezone.utc)
        current_value = 110000.00
        with patch("homestake.database.client.Session") as mock_session:
            mock_session.return_value.__enter__.return_value.add = MagicMock()
            mock_session.return_value.__enter__.return_value.commit.side_effect = SQLAlchemyError(
                "mock")
            mock_session.return_value.__enter__.return_value.rollback = MagicMock()

            with self.assertRaisesRegex(DatabaseClientError, const.PROPERTY_CREATE_ERROR_MSG):
                self.db_client.create_property(
                    property_name, address, purchase_price, purchase_date, current_value)

            mock_session.return_value.__enter__.return_value.rollback.assert_called_once()

    def test_get_property_by_address(self):
        address = "123 Test St"
        purchase_price = 100000.00
        purchase_date = datetime.now(timezone.utc)
        current_value = 110000.00
        with patch("homestake.database.client.Session") as mock_session:
            mock_session.return_value.__enter__.return_value.query = MagicMock(
                return_value=MagicMock(
                    filter_by=MagicMock(
                        return_value=MagicMock(
                            first=MagicMock(return_value=Property(
                                address=address,
                                purchase_date=purchase_date,
                                purchase_price=purchase_price,
                                current_value=current_value
                            ))
                        )
                    )
                )
            )

            result = self.db_client.get_property_by_address(address)
            self.assertEqual(result["address"], address)
            self.assertEqual(result["purchase_price"], purchase_price)
            self.assertEqual(result["purchase_date"],
                             purchase_date.isoformat())
            self.assertEqual(result["current_value"], current_value)

            mock_session.return_value.__enter__.return_value.query.assert_called_once()

    def test_get_property_by_id(self):
        property_id = 1
        address = "123 Test St"
        purchase_price = 100000.00
        purchase_date = datetime.now(timezone.utc)
        current_value = 110000.00
        with patch("homestake.database.client.Session") as mock_session:
            mock_session.return_value.__enter__.return_value.query = MagicMock(
                return_value=MagicMock(
                    filter_by=MagicMock(
                        return_value=MagicMock(
                            first=MagicMock(return_value=Property(
                                id=property_id,
                                address=address,
                                purchase_date=purchase_date,
                                purchase_price=purchase_price,
                                current_value=current_value
                            ))
                        )
                    )
                )
            )

            result = self.db_client.get_property_by_id(property_id)
            self.assertEqual(result["id"], property_id)
            self.assertEqual(result["address"], address)
            self.assertEqual(result["purchase_price"], purchase_price)
            self.assertEqual(result["purchase_date"],
                             purchase_date.isoformat())
            self.assertEqual(result["current_value"], current_value)

            mock_session.return_value.__enter__.return_value.query.assert_called_once()

    def test_get_property_by_name(self):
        property_id = 1
        property_name = "primary residence"
        address = "123 Test St"
        purchase_price = 100000.00
        purchase_date = datetime.now(timezone.utc)
        current_value = 110000.00
        with patch("homestake.database.client.Session") as mock_session:
            mock_session.return_value.__enter__.return_value.query = MagicMock(
                return_value=MagicMock(
                    filter_by=MagicMock(
                        return_value=MagicMock(
                            first=MagicMock(return_value=Property(
                                id=property_id,
                                name=property_name,
                                address=address,
                                purchase_date=purchase_date,
                                purchase_price=purchase_price,
                                current_value=current_value
                            ))
                        )
                    )
                )
            )

            result = self.db_client.get_property_by_name(property_name)
            self.assertEqual(result["id"], property_id)
            self.assertEqual(result["name"], property_name)
            self.assertEqual(result["address"], address)
            self.assertEqual(result["purchase_price"], purchase_price)
            self.assertEqual(result["purchase_date"],
                             purchase_date.isoformat())
            self.assertEqual(result["current_value"], current_value)

            mock_session.return_value.__enter__.return_value.query.assert_called_once()

    def test_update_property(self):
        old_address = "123 Test St"
        new_address = "456 Test St"
        property_id = 1
        purchase_price = 100000.00
        purchase_date = datetime.now(timezone.utc)
        current_value = 110000.00
        with patch("homestake.database.client.Session") as mock_session:
            test_property = Property(
                id=property_id, address=old_address, purchase_date=purchase_date, purchase_price=purchase_price, current_value=current_value)

            mock_query = MagicMock()
            mock_session.return_value.__enter__.return_value.query.side_effect = [
                mock_query, mock_query]
            mock_query.filter_by.return_value.first.return_value = test_property

            self.assertEqual(test_property.address, old_address)
            result = self.db_client.update_property(
                property_id, address=new_address)
            self.assertEqual(result["id"], property_id)
            self.assertEqual(result["address"], new_address)
            self.assertEqual(result["purchase_price"], purchase_price)
            self.assertEqual(result["purchase_date"],
                             purchase_date.isoformat())
            self.assertEqual(result["current_value"], current_value)

            self.assertEqual(mock_query.filter_by.call_count, 1)
            mock_query.filter_by.assert_any_call(id=property_id)
            mock_session.return_value.__enter__.return_value.commit.assert_called_once()

    def test_update_property_sqlalchemy_error(self):
        old_address = "123 Test St"
        new_address = "456 Test St"
        property_id = 1
        purchase_price = 100000.00
        purchase_date = datetime.now(timezone.utc)
        current_value = 110000.00
        with patch("homestake.database.client.Session") as mock_session:
            test_property = Property(
                address=old_address, purchase_date=purchase_date, purchase_price=purchase_price, current_value=current_value)

            mock_query = MagicMock()
            mock_session.return_value.__enter__.return_value.query.side_effect = [
                mock_query, mock_query]
            mock_query.filter_by.return_value.first.return_value = test_property
            mock_session.return_value.__enter__.return_value.commit.side_effect = SQLAlchemyError(
                "mock")

            with self.assertRaisesRegex(DatabaseClientError, const.PROPERTY_UPDATE_ERROR_MSG):
                self.db_client.update_property(
                    property_id, address=new_address)

            self.assertEqual(mock_query.filter_by.call_count, 1)
            mock_query.filter_by.assert_any_call(id=property_id)
            mock_session.return_value.__enter__.return_value.rollback.assert_called_once()

    def test_update_property_not_found(self):
        new_address = "456 Test St"
        property_id = 1
        with patch("homestake.database.client.Session") as mock_session:
            mock_query = MagicMock()
            mock_session.return_value.__enter__.return_value.query.side_effect = [
                mock_query, mock_query]
            mock_query.filter_by.return_value.first.return_value = None

            with self.assertRaisesRegex(DatabaseClientError, const.PROPERTY_ID_NOT_FOUND.format(property_id)):
                self.db_client.update_property(
                    property_id, address=new_address)

            self.assertEqual(mock_query.filter_by.call_count, 1)
            mock_query.filter_by.assert_any_call(id=property_id)
            mock_session.return_value.__enter__.return_value.commit.assert_not_called()
            mock_session.return_value.__enter__.return_value.rollback.assert_not_called()

    def test_delete_property(self):
        property_id = 1
        purchase_date = datetime.now(timezone.utc)
        with patch("homestake.database.client.Session") as mock_session:
            mock_session.return_value.__enter__.return_value.query.return_value.filter_by.return_value.first.return_value = Property(
                id=property_id,
                purchase_date=purchase_date
            )
            mock_session.return_value.__enter__.return_value.delete = MagicMock()

            self.db_client.delete_property(property_id)

            mock_session.return_value.__enter__.return_value.query.assert_called_once()
            mock_session.return_value.__enter__.return_value.query.return_value.filter_by.assert_called_once_with(
                id=property_id)
            mock_session.return_value.__enter__.return_value.delete.assert_called_once()

    def test_delete_property_sqlalchemy_error(self):
        property_id = 1
        with patch("homestake.database.client.Session") as mock_session:
            mock_session.return_value.__enter__.return_value.query.return_value.filter_by.return_value.first.return_value = Property()
            mock_session.return_value.__enter__.return_value.delete.side_effect = SQLAlchemyError(
                "mock")
            mock_session.return_value.__enter__.return_value.rollback = MagicMock()

            with self.assertRaisesRegex(DatabaseClientError, const.PROPERTY_DELETE_ERROR_MSG):
                self.db_client.delete_property(property_id)

            mock_session.return_value.__enter__.return_value.rollback.assert_called_once()

    def test_delete_property_not_found(self):
        property_id = 1
        with patch("homestake.database.client.Session") as mock_session:
            mock_session.return_value.__enter__.return_value.query.return_value.filter_by.return_value.first.return_value = None

            with self.assertRaisesRegex(DatabaseClientError, const.PROPERTY_ID_NOT_FOUND.format(property_id)):
                self.db_client.delete_property(property_id)

            mock_session.return_value.__enter__.return_value.query.return_value.filter_by.assert_called_once_with(
                id=property_id)
            mock_session.return_value.__enter__.return_value.commit.assert_not_called()
            mock_session.return_value.__enter__.return_value.rollback.assert_not_called()


class TestTransaction(unittest.TestCase):
    def setUp(self):
        self.db_client = DatabaseClient()

    def test_create_transaction(self):
        transaction_id = 1
        amount = 9001.00
        user_id = 2
        current_date = datetime.now(timezone.utc)
        account_id = 3
        with patch("homestake.database.client.Session") as mock_session:
            mock_session.return_value.__enter__.return_value.add = MagicMock(
                side_effect=lambda transaction: setattr(
                    transaction, "id", transaction_id) or setattr(transaction, "date", current_date)
            )
            mock_session.return_value.__enter__.return_value.commit = MagicMock()

            result = self.db_client.create_transaction(
                amount, current_date, user_id, account_id)

            self.assertEqual(result["id"], transaction_id)
            self.assertEqual(result["amount"], amount)
            self.assertEqual(result["date"], current_date.isoformat())
            self.assertEqual(result["user_id"], user_id)
            self.assertEqual(result["account_id"], account_id)

            mock_session.return_value.__enter__.return_value.add.assert_called_once()
            mock_session.return_value.__enter__.return_value.commit.assert_called_once()

    def test_create_transaction_integrity_error(self):
        amount = 9001.00
        user_id = 1
        current_date = datetime.now(timezone.utc)
        account_id = 1
        with patch("homestake.database.client.Session") as mock_session:
            mock_session.return_value.__enter__.return_value.add = MagicMock()
            mock_session.return_value.__enter__.return_value.commit.side_effect = IntegrityError(
                "mock", "mock", "mock")
            mock_session.return_value.__enter__.return_value.rollback = MagicMock()

            with self.assertRaisesRegex(DatabaseClientError, const.TRANSACTION_CREATE_ERROR_MSG):
                self.db_client.create_transaction(
                    amount, current_date, user_id, account_id)

            mock_session.return_value.__enter__.return_value.rollback.assert_called_once()

    def test_create_transaction_sqlalchemy_error(self):
        amount = 9001.00
        user_id = 1
        current_date = datetime.now(timezone.utc)
        account_id = 1
        with patch("homestake.database.client.Session") as mock_session:
            mock_session.return_value.__enter__.return_value.add = MagicMock()
            mock_session.return_value.__enter__.return_value.commit.side_effect = SQLAlchemyError(
                "mock")
            mock_session.return_value.__enter__.return_value.rollback = MagicMock()

            with self.assertRaisesRegex(DatabaseClientError, const.TRANSACTION_CREATE_ERROR_MSG):
                self.db_client.create_transaction(
                    amount, current_date, user_id, account_id)

            mock_session.return_value.__enter__.return_value.rollback.assert_called_once()

    def test_get_transaction_by_id(self):
        transaction_id = 1
        amount = 100.00
        with patch("homestake.database.client.Session") as mock_session:
            mock_session.return_value.__enter__.return_value.query = MagicMock(
                return_value=MagicMock(
                    filter_by=MagicMock(
                        return_value=MagicMock(
                            first=MagicMock(return_value=Transaction(
                                id=transaction_id,
                                date=datetime.now(timezone.utc),
                                amount=amount
                            ))
                        )
                    )
                )
            )

            account = self.db_client.get_transaction_by_id(transaction_id)
            self.assertTrue(account["id"], transaction_id)
            self.assertTrue(account["amount"], amount)

            mock_session.return_value.__enter__.return_value.query.assert_called

    def test_list_transactions_by_user(self):
        transaction_id = 1
        user_id = 1
        with patch("homestake.database.client.Session") as mock_session:
            mock_session.return_value.__enter__.return_value.query = MagicMock(
                return_value=MagicMock(
                    filter_by=MagicMock(
                        return_value=MagicMock(
                            all=MagicMock(return_value=[Transaction(
                                id=transaction_id,
                                date=datetime.now(timezone.utc),
                                user_id=user_id
                            )])
                        )
                    )
                )
            )

            transactions = self.db_client.list_transactions_by_user(user_id)
            self.assertTrue(isinstance(transactions, List))
            self.assertTrue(all(
                transaction["id"] == transaction_id and transaction["user_id"] for transaction in transactions))

            mock_session.return_value.__enter__.return_value.query.assert_called_once()

    def test_list_transactions_by_account(self):
        transaction_id = 1
        account_id = 1
        user_id = 1
        with patch("homestake.database.client.Session") as mock_session:
            mock_session.return_value.__enter__.return_value.query = MagicMock(
                return_value=MagicMock(
                    filter_by=MagicMock(
                        return_value=MagicMock(
                            first=MagicMock(
                                return_value=Account(
                                    transactions=[
                                        Transaction(
                                            id=transaction_id,
                                            date=datetime.now(timezone.utc),
                                            account_id=account_id,
                                            user_id=user_id
                                        )
                                    ]
                                )
                            )
                        )
                    )
                )
            )

            transactions = self.db_client.list_transactions_by_account(
                account_id)
            self.assertTrue(isinstance(transactions, List))
            self.assertTrue(all(
                transaction["id"] == transaction_id and transaction["user_id"] for transaction in transactions))

            mock_session.return_value.__enter__.return_value.query.assert_called_once()

    def test_list_transactions_by_account_account_no_exist(self):
        account_id = 1
        with patch("homestake.database.client.Session") as mock_session:
            mock_session.return_value.__enter__.return_value.query = MagicMock(
                return_value=MagicMock(
                    filter_by=MagicMock(
                        return_value=MagicMock(
                            first=MagicMock(
                                return_value=None
                            )
                        )
                    )
                )
            )

            with self.assertRaisesRegex(DatabaseClientError, const.ACCOUNT_ID_NOT_FOUND.format(account_id)):
                self.db_client.list_transactions_by_account(account_id)

            mock_session.return_value.__enter__.return_value.query.assert_called_once()

    def test_update_transaction(self):
        old_amount = 9001.00
        new_amount = 9002.00
        transaction_id = 1
        with patch("homestake.database.client.Session") as mock_session:
            test_transaction = Transaction(
                id=transaction_id, date=datetime.now(timezone.utc), amount=old_amount)

            mock_query = MagicMock()
            mock_session.return_value.__enter__.return_value.query.side_effect = [
                mock_query, mock_query]
            mock_query.filter_by.return_value.first.return_value = test_transaction

            self.assertEqual(test_transaction.amount, old_amount)
            result = self.db_client.update_transaction(
                transaction_id, amount=new_amount)

            self.assertEqual(result["id"], transaction_id)
            self.assertEqual(result["amount"], new_amount)

            self.assertEqual(mock_query.filter_by.call_count, 1)
            mock_query.filter_by.assert_any_call(id=transaction_id)
            mock_session.return_value.__enter__.return_value.commit.assert_called_once()

    def test_update_transaction_sqlalchemy_error(self):
        old_amount = 9001.00
        new_amount = 9002.00
        transaction_id = 1
        with patch("homestake.database.client.Session") as mock_session:
            test_transaction = Transaction(
                id=transaction_id, amount=old_amount)

            mock_query = MagicMock()
            mock_session.return_value.__enter__.return_value.query.side_effect = [
                mock_query, mock_query]
            mock_query.filter_by.return_value.first.return_value = test_transaction
            mock_session.return_value.__enter__.return_value.commit.side_effect = SQLAlchemyError(
                "mock")

            with self.assertRaisesRegex(DatabaseClientError, const.TRANSACTION_UPDATE_ERROR_MSG):
                self.db_client.update_transaction(
                    transaction_id, amount=new_amount)

            self.assertEqual(mock_query.filter_by.call_count, 1)
            mock_query.filter_by.assert_any_call(id=transaction_id)
            mock_session.return_value.__enter__.return_value.rollback.assert_called_once()

    def test_update_transaction_not_found(self):
        new_amount = 9002.00
        transaction_id = 1
        with patch("homestake.database.client.Session") as mock_session:
            mock_query = MagicMock()
            mock_session.return_value.__enter__.return_value.query.side_effect = [
                mock_query, mock_query]
            mock_query.filter_by.return_value.first.return_value = None

            with self.assertRaisesRegex(DatabaseClientError, const.TRANSACTION_ID_NOT_FOUND.format(transaction_id)):
                self.db_client.update_transaction(
                    transaction_id, amount=new_amount)

            self.assertEqual(mock_query.filter_by.call_count, 1)
            mock_query.filter_by.assert_any_call(id=transaction_id)
            mock_session.return_value.__enter__.return_value.commit.assert_not_called()
            mock_session.return_value.__enter__.return_value.rollback.assert_not_called()

    def test_delete_transaction(self):
        transaction_id = 1
        with patch("homestake.database.client.Session") as mock_session:
            mock_session.return_value.__enter__.return_value.query.return_value.filter_by.return_value.first.return_value = Transaction(
                date=datetime.now(timezone.utc))
            mock_session.return_value.__enter__.return_value.delete = MagicMock()

            self.db_client.delete_transaction(transaction_id)

            mock_session.return_value.__enter__.return_value.query.assert_called_once()
            mock_session.return_value.__enter__.return_value.query.return_value.filter_by.assert_called_once_with(
                id=transaction_id)
            mock_session.return_value.__enter__.return_value.delete.assert_called_once()

    def test_delete_transaction_sqlalchemy_error(self):
        transaction_id = 1
        with patch("homestake.database.client.Session") as mock_session:
            mock_session.return_value.__enter__.return_value.query.return_value.filter_by.return_value.first.return_value = Transaction()
            mock_session.return_value.__enter__.return_value.delete.side_effect = SQLAlchemyError(
                "mock")
            mock_session.return_value.__enter__.return_value.rollback = MagicMock()

            with self.assertRaisesRegex(DatabaseClientError, const.TRANSACTION_DELETE_ERROR_MSG):
                self.db_client.delete_transaction(transaction_id)

            mock_session.return_value.__enter__.return_value.rollback.assert_called_once()

    def test_delete_transaction_not_found(self):
        transaction_id = 1
        with patch("homestake.database.client.Session") as mock_session:
            mock_session.return_value.__enter__.return_value.query.return_value.filter_by.return_value.first.return_value = None

            with self.assertRaisesRegex(DatabaseClientError, const.TRANSACTION_ID_NOT_FOUND.format(transaction_id)):
                self.db_client.delete_transaction(transaction_id)

            mock_session.return_value.__enter__.return_value.query.return_value.filter_by.assert_called_once_with(
                id=transaction_id)
            mock_session.return_value.__enter__.return_value.commit.assert_not_called()
            mock_session.return_value.__enter__.return_value.rollback.assert_not_called()

    def test_list_transactions(self):
        current_date = datetime.now(timezone.utc)
        with patch("homestake.database.client.Session") as mock_session:
            mock_query = MagicMock()
            mock_query.all.return_value = [
                Transaction(date=current_date)]
            mock_session.return_value.__enter__.return_value.query.return_value = mock_query

            result = self.db_client.list_transactions()
            self.assertTrue(isinstance(result, List))
            self.assertTrue(
                all(transaction["date"] == current_date.isoformat() for transaction in result))

            mock_session.return_value.__enter__.return_value.query.assert_called_once()
            mock_query.all.assert_called_once()


class TestUser(unittest.TestCase):
    def setUp(self):
        self.db_client = DatabaseClient()

    def test_create_user_success_required_args(self):
        user_id = 1
        user_name = "testuser"
        email = "test@example.com"
        password = "secretpassword"
        stake = 100
        with patch("homestake.database.client.Session") as mock_session:
            mock_session.return_value.__enter__.return_value.add = MagicMock(
                side_effect=lambda user: setattr(user, "id", user_id))
            mock_session.return_value.__enter__.return_value.commit = MagicMock()

            user = self.db_client.create_user(
                user_name, email, password, stake)
            self.assertEqual(user["id"], user_id)
            self.assertEqual(user["user_name"], user_name)
            self.assertEqual(user["email"], email)
            self.assertEqual(user["stake"], stake)

            mock_session.return_value.__enter__.return_value.add.assert_called_once()
            mock_session.return_value.__enter__.return_value.commit.assert_called_once()

    def test_create_user_success_optional_args(self):
        user_id = 1
        user_name = "testuser"
        email = "test@example.com"
        password = "secretpassword"
        stake = 100
        mortgage_id = 1
        property_id = 2
        with patch("homestake.database.client.Session") as mock_session:
            mock_session.return_value.__enter__.return_value.add = MagicMock(
                side_effect=lambda user: setattr(user, "id", user_id))
            mock_session.return_value.__enter__.return_value.commit = MagicMock()

            user = self.db_client.create_user(
                user_name, email, password, stake, mortgage_id, property_id)
            self.assertEqual(user["id"], user_id)
            self.assertEqual(user["user_name"], user_name)
            self.assertEqual(user["email"], email)
            self.assertEqual(user["stake"], stake)
            self.assertEqual(user["mortgage_id"], mortgage_id)
            self.assertEqual(user["property_id"], property_id)

            mock_session.return_value.__enter__.return_value.add.assert_called_once()
            mock_session.return_value.__enter__.return_value.commit.assert_called_once()

    def test_create_user_integrity_error_name_exists(self):
        user_name = "testuser"
        email = "test@example.com"
        stake = 100
        mortgage_id = 1
        with patch("homestake.database.client.Session") as mock_session:
            mock_session.return_value.__enter__.return_value.add = MagicMock()
            mock_session.return_value.__enter__.return_value.commit.side_effect = IntegrityError(
                f"{const.DB_ENTRY_EXISTS_MSG}: user.user_name", "mock", "mock")
            mock_session.return_value.__enter__.return_value.rollback = MagicMock()

            with self.assertRaisesRegex(DatabaseDuplicationError, const.USER_EXISTS_MSG):
                self.db_client.create_user(
                    user_name, email, stake, mortgage_id)

            mock_session.return_value.__enter__.return_value.rollback.assert_called_once()

    def test_create_user_integrity_error_email_exists(self):
        user_name = "testuser"
        email = "test@example.com"
        stake = 100
        mortgage_id = 1
        with patch("homestake.database.client.Session") as mock_session:
            mock_session.return_value.__enter__.return_value.add = MagicMock()
            mock_session.return_value.__enter__.return_value.commit.side_effect = IntegrityError(
                f"{const.DB_ENTRY_EXISTS_MSG}: user.email", "mock", "mock")
            mock_session.return_value.__enter__.return_value.rollback = MagicMock()

            with self.assertRaisesRegex(DatabaseDuplicationError, const.USER_EXISTS_MSG):
                self.db_client.create_user(
                    user_name, email, stake, mortgage_id)

            mock_session.return_value.__enter__.return_value.rollback.assert_called_once()

    def test_create_user_sqlalchemy_error(self):
        user_name = "testuser"
        email = "test@example.com"
        stake = 100
        mortgage_id = 1
        with patch("homestake.database.client.Session") as mock_session:
            mock_session.return_value.__enter__.return_value.add = MagicMock()
            mock_session.return_value.__enter__.return_value.commit.side_effect = SQLAlchemyError(
                "mock")
            mock_session.return_value.__enter__.return_value.rollback = MagicMock()

            with self.assertRaisesRegex(DatabaseClientError, const.USER_CREATE_ERROR_MSG):
                self.db_client.create_user(
                    user_name, email, stake, mortgage_id)

            mock_session.return_value.__enter__.return_value.rollback.assert_called_once()

    def test_get_user_by_name(self):
        user_name = "testuser"
        with patch("homestake.database.client.Session") as mock_session:
            mock_session.return_value.__enter__.return_value.query = MagicMock(
                return_value=MagicMock(
                    filter_by=MagicMock(
                        return_value=MagicMock(
                            first=MagicMock(return_value=User(
                                user_name=user_name
                            ))
                        )
                    )
                )
            )

            result = self.db_client.get_user_by_name(user_name)
            self.assertEqual(result["user_name"], user_name)

            mock_session.return_value.__enter__.return_value.query.assert_called_once()

    def test_get_user_by_id(self):
        user_id = 1
        with patch("homestake.database.client.Session") as mock_session:
            mock_session.return_value.__enter__.return_value.query = MagicMock(
                return_value=MagicMock(
                    filter_by=MagicMock(
                        return_value=MagicMock(
                            first=MagicMock(return_value=User(
                                id=user_id
                            ))
                        )
                    )
                )
            )

            result = self.db_client.get_user_by_id(user_id)
            self.assertEqual(result["id"], user_id)

            mock_session.return_value.__enter__.return_value.query.assert_called_once()

    def test_update_user(self):
        old_user_name = "testuser"
        new_user_name = "newuser"
        user_id = 1
        with patch("homestake.database.client.Session") as mock_session:
            test_user = User(
                id=user_id, user_name=old_user_name)

            mock_query = MagicMock()
            mock_session.return_value.__enter__.return_value.query.side_effect = [
                mock_query, mock_query]
            mock_query.filter_by.return_value.first.return_value = test_user

            self.assertEqual(test_user.user_name, old_user_name)
            result = self.db_client.update_user(
                user_id, user_name=new_user_name)
            self.assertEqual(result["id"], user_id)
            self.assertEqual(result["user_name"], new_user_name)

            self.assertEqual(mock_query.filter_by.call_count, 1)
            mock_query.filter_by.assert_any_call(id=user_id)
            mock_session.return_value.__enter__.return_value.commit.assert_called_once()

    def test_update_user_sqlalchemy_error(self):
        old_user_name = "testuser"
        new_user_name = "newuser"
        user_id = 1
        with patch("homestake.database.client.Session") as mock_session:
            test_user = User(
                id=user_id, user_name=old_user_name)

            mock_query = MagicMock()
            mock_session.return_value.__enter__.return_value.query.side_effect = [
                mock_query, mock_query]
            mock_query.filter_by.return_value.first.return_value = test_user
            mock_session.return_value.__enter__.return_value.commit.side_effect = SQLAlchemyError(
                "mock")

            with self.assertRaisesRegex(DatabaseClientError, const.USER_UPDATE_ERROR_MSG):
                self.db_client.update_user(user_id, user_name=new_user_name)

            self.assertEqual(mock_query.filter_by.call_count, 1)
            mock_query.filter_by.assert_any_call(id=user_id)
            mock_session.return_value.__enter__.return_value.rollback.assert_called_once()

    def test_update_user_not_found(self):
        new_user_name = "newuser"
        user_id = 1
        with patch("homestake.database.client.Session") as mock_session:
            mock_query = MagicMock()
            mock_session.return_value.__enter__.return_value.query.side_effect = [
                mock_query, mock_query]
            mock_query.filter_by.return_value.first.return_value = None

            with self.assertRaisesRegex(DatabaseClientError, const.USER_ID_NOT_FOUND.format(user_id)):
                self.db_client.update_user(user_id, user_name=new_user_name)

            self.assertEqual(mock_query.filter_by.call_count, 1)
            mock_query.filter_by.assert_any_call(id=user_id)
            mock_session.return_value.__enter__.return_value.commit.assert_not_called()
            mock_session.return_value.__enter__.return_value.rollback.assert_not_called()

    def test_delete_user(self):
        user_id = 1
        with patch("homestake.database.client.Session") as mock_session:
            mock_session.return_value.__enter__.return_value.query.return_value.filter_by.return_value.first.return_value = User()
            mock_session.return_value.__enter__.return_value.delete = MagicMock()

            self.db_client.delete_user(user_id)

            mock_session.return_value.__enter__.return_value.query.assert_called_once()
            mock_session.return_value.__enter__.return_value.query.return_value.filter_by.assert_called_once_with(
                id=user_id)
            mock_session.return_value.__enter__.return_value.delete.assert_called_once()

    def test_delete_user_sqlalchemy_error(self):
        user_id = 1
        with patch("homestake.database.client.Session") as mock_session:
            mock_session.return_value.__enter__.return_value.query.return_value.filter_by.return_value.first.return_value = User()
            mock_session.return_value.__enter__.return_value.delete.side_effect = SQLAlchemyError(
                "mock")
            mock_session.return_value.__enter__.return_value.rollback = MagicMock()

            with self.assertRaisesRegex(DatabaseClientError, const.USER_DELETE_ERROR_MSG):
                self.db_client.delete_user(user_id)

            mock_session.return_value.__enter__.return_value.rollback.assert_called_once()

    def test_delete_user_not_found(self):
        user_id = 1
        with patch("homestake.database.client.Session") as mock_session:
            mock_session.return_value.__enter__.return_value.query.return_value.filter_by.return_value.first.return_value = None

            with self.assertRaisesRegex(DatabaseClientError, const.USER_ID_NOT_FOUND.format(user_id)):
                self.db_client.delete_user(user_id)

            mock_session.return_value.__enter__.return_value.query.return_value.filter_by.assert_called_once_with(
                id=user_id)
            mock_session.return_value.__enter__.return_value.commit.assert_not_called()
            mock_session.return_value.__enter__.return_value.rollback.assert_not_called()

    def test_list_users(self):
        user_id = 1
        user_name = "testuser"
        with patch("homestake.database.client.Session") as mock_session:
            mock_query = MagicMock()
            mock_query.all.return_value = [
                User(id=user_id, user_name=user_name)]
            mock_session.return_value.__enter__.return_value.query.return_value = mock_query

            result = self.db_client.list_users()
            self.assertTrue(isinstance(result, List))
            self.assertTrue(
                all(user["id"] == user_id and user["user_name"] == user_name for user in result))

            mock_session.return_value.__enter__.return_value.query.assert_called_once()
            mock_query.all.assert_called_once()
