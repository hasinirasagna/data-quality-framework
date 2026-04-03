import great_expectations as gx
import os


def setup_ge():
    base_path = os.path.dirname(os.path.dirname(__file__))

    context = gx.get_context()

    data_path = os.path.join(
        base_path, "data/validated/clean_customers.csv"
    )

    datasource_name = "customer_data_source"
    asset_name = "customer_data_asset"
    suite_name = "customer_data_validation"

    datasource = context.sources.add_or_update_pandas(datasource_name)
    print("ℹ️ Datasource ready")

    data_asset = datasource.add_csv_asset(
        name=asset_name,
        filepath_or_buffer=data_path
    )
    print("ℹ️ Data asset ready")

    batch_request = data_asset.build_batch_request()

    context.add_or_update_expectation_suite(
        expectation_suite_name=suite_name
    )

    validator = context.get_validator(
        batch_request=batch_request,
        expectation_suite_name=suite_name
    )

    validator.expect_column_values_to_not_be_null("customer_id")
    validator.expect_column_values_to_not_be_null("customer_unique_id")
    validator.expect_column_values_to_be_unique("customer_id")
    validator.expect_column_values_to_not_be_null("customer_zip_code_prefix")

    validator.expect_column_values_to_match_regex(
        "customer_zip_code_prefix", r"^\d+$"
    )

    validator.expect_column_value_lengths_to_equal("customer_state", 2)

    validator.save_expectation_suite()

    results = validator.validate()

    print("\n📊 Great Expectations Result:")
    print(results)


if __name__ == "__main__":
    setup_ge()