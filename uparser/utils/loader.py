from django.core.exceptions import ObjectDoesNotExist, ValidationError

from parser.models import OrderLine
from utils.data import OrderLineData, make_dataframe
from utils.logging_config import configure_logging, logging
from utils.online import read_google_spreadsheet

configure_logging()


def load2django():
    """Main ETL process."""
    logging.debug('Starting ETL....')
    google_data = read_google_spreadsheet()
    df = make_dataframe(google_data)
    for _, row in df.iterrows():
        line = OrderLineData(*[value for _, value in row.items()])
        try:
            order_line = OrderLine.objects.get(line_no=line.line_no, order_no=line.order_no)
            order_line.value_usd = line.value_usd
            order_line.value_rub = line.value_rub
            order_line.due_date = line.due_date
        except ObjectDoesNotExist:
            order_line = OrderLine.objects.create(**line.__dict__)

        try:
            order_line.full_clean()
            order_line.save()
        except ValidationError as e:
            logging.warning(
                'Data integrity issue with: {}. Record was not saved.'.format(order_line))
            logging.error(e.error_dict)
