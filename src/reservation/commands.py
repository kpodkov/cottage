import click
import os
import pandas

from slugify import slugify
from random import seed, randint
from datetime import datetime
from pathlib import Path

from ..common.colors import TerminalColours


@click.group(help="Reservation operations", invoke_without_command=False)
def reservation():
    pass


@reservation.command(name="load",
                     short_help="Converts the input reservation.csv from Airbnb into an Excel file, split with a sheet for each Listing.")
@click.option('--csv-path', '-c', 'csv_path', help='Path to reservations.csv from Airbnb console', prompt=True)
@click.option('--output-path', '-o', 'output_path', help='Desired output .xlsx path', prompt=False,
              default='./output/reservations.xlsx')
@click.pass_context
def create_overview_excel(context: click.Context, csv_path: str, output_path: str) -> None:
    def date_difference(start_date: str, end_date: str) -> int:
        return (datetime.strptime(end_date, '%m-%d-%Y') - datetime.strptime(start_date, '%m-%d-%Y')).days

    def transform_dataframe(input_df: pandas.DataFrame) -> pandas.DataFrame:
        seed(1)
        input_df = input_df.assign(start_dow=input_df['Start date'].map(
            lambda value: datetime.strptime(value, '%m-%d-%Y').strftime('%A')))
        input_df = input_df.assign(
            end_dow=input_df['End date'].map(lambda value: datetime.strptime(value, '%m-%d-%Y').strftime('%A')))
        input_df['door_code'] = [randint(1000, 9999) for i in input_df.index]
        input_df['num_of_nights'] = input_df.apply(
            lambda row: date_difference(start_date=row['Start date'], end_date=row['End date']), axis=1)
        input_df['Start date'] = input_df['Start date'].map(
            lambda value: datetime.strptime(value, '%m-%d-%Y').strftime('%Y-%m-%d'))
        input_df['End date'] = input_df['End date'].map(
            lambda value: datetime.strptime(value, '%m-%d-%Y').strftime('%Y-%m-%d'))

        df_output = pandas.DataFrame()
        df_output['Guest Name'] = input_df['Guest name']
        df_output['Start DOW'] = input_df['start_dow']
        df_output['Start Date'] = input_df['Start date']
        df_output['End Date'] = input_df['End date']
        df_output['END DOW'] = input_df['end_dow']
        df_output['Door Code'] = input_df['door_code']
        df_output['Total Payout'] = input_df['Earnings']
        df_output['Email'] = ''
        df_output['House Manual Sent'] = ''
        df_output['Door Code Sent'] = ''
        df_output['Special Notes'] = ''
        return df_output

    if os.path.exists(csv_path):
        try:
            input_df = pandas.read_csv(csv_path)
            listings = input_df['Listing'].unique()
            Path('./output/').mkdir(exist_ok=True)
            output_xlsx = pandas.ExcelWriter(path=output_path, engine='openpyxl')
            for listing in listings:
                filtered_df = input_df[input_df['Listing'] == listing]
                transform_dataframe(filtered_df).to_excel(output_xlsx,
                                                          sheet_name=slugify(listing, max_length=30),
                                                          index=False)
            output_xlsx.save()
            print(f'{TerminalColours.GREEN}Generated output file: {output_path}{TerminalColours.ENDC}')
        except PermissionError as ex:
            context.fail(f'The output file is maybe in use by something else: {ex}')
        except Exception as ex:
            context.fail(f'Error creating .xlsx file {ex}')
    else:
        context.fail(f'Failed to read csv from path: {csv_path}')
