from metrocar.invoices.models import Invoice
from metrocar.cars.models import FuelBill

from testproject.helpers import get_cars
from testproject.helpers import UserEnabledTestCase

class InvoiceEnabledTestCase(UserEnabledTestCase):
    def setUp(self):
        super(InvoiceEnabledTestCase, self).setUp()
        car_model, car, parking = get_cars()
        
        self.acc_act_1 = FuelBill(account=self.user.account,
            money_amount=400, code='123', approved=True,
            car=car, fuel=car.model.main_fuel, liter_count=10, place='Benzinka')
        self.acc_act_1.save()
        
        self.acc_act_2 = FuelBill(account=self.user.account,
            money_amount=400, code='123', approved=False,
            car=car, fuel=car.model.main_fuel, liter_count=10, place='Benzinka')
        self.acc_act_2.save()
        
        self.acc_act_3 = FuelBill(account=self.user.account,
            money_amount=400, code='123', approved=True,
            car=car, fuel=car.model.main_fuel, liter_count=10, place='Benzinka',
            credited=True)
        self.acc_act_3.save()
        
        # magic done via post save signal
        self.invoice = Invoice.objects.create(user=self.user)
        
    def tearDown(self):
        super(InvoiceEnabledTestCase, self).tearDown()
        self.acc_act_1.delete()
        self.acc_act_2.delete()
        self.acc_act_3.delete()