from django.shortcuts import get_object_or_404

from .models import NDS, ElectricityMeteringPoint, Tariff


def calculation_tariff(point_id):
    """The function for determining the cost of the tariff selected at the
    ElectricityMeteringPoint. The VAT amount is deducted from the tariffs for
    urban and rural populations, since it was originally included in the tariffs.
    """
    point = get_object_or_404(ElectricityMeteringPoint, pk=point_id)
    tariff = Tariff.objects.all()[0]
    if point.tariff == 'urban_tariff':
        tariff1 = tariff.urban_tariff_1 - tariff.urban_tariff_1 * NDS / (100 + NDS)
        tariff2 = tariff.urban_tariff_2 - tariff.urban_tariff_2 * NDS / (100 + NDS)
        tariff3 = tariff.urban_tariff_3 - tariff.urban_tariff_3 * NDS / (100 + NDS)
        is_population = True
        return (round(tariff1, 5),
                round(tariff2, 5),
                round(tariff3, 5),
                is_population,)
    elif point.tariff == 'rural_tariff':
        tariff1 = tariff.rural_tariff_1 - tariff.rural_tariff_1 * NDS / (100 + NDS)
        tariff2 = tariff.rural_tariff_2 - tariff.rural_tariff_2 * NDS / (100 + NDS)
        tariff3 = tariff.rural_tariff_3 - tariff.rural_tariff_3 * NDS / (100 + NDS)
        is_population = True
        return (round(tariff1, 5),
                round(tariff2, 5),
                round(tariff3, 5),
                is_population,)
    elif point.tariff == 'low_voltage_tariff':
        is_population = False
        return (tariff.low_voltage_tariff,
                tariff.low_voltage_tariff,
                tariff.low_voltage_tariff,
                is_population,)
    elif point.tariff == 'medium_voltage_tariff_1':
        is_population = False
        return (tariff.medium_voltage_tariff_1,
                tariff.medium_voltage_tariff_1,
                tariff.medium_voltage_tariff_1,
                is_population,)
    elif point.tariff == 'medium_voltage_tariff_2':
        is_population = False
        return (tariff.medium_voltage_tariff_2,
                tariff.medium_voltage_tariff_2,
                tariff.medium_voltage_tariff_2,
                is_population,)
    elif point.tariff == 'high_voltage_tariff':
        is_population = False
        return (tariff.high_voltage_tariff,
                tariff.high_voltage_tariff,
                tariff.high_voltage_tariff,
                is_population,)
    elif point.tariff == 'tariff-free':
        is_population = False
        return (0, 0, 0, is_population,)


def calculation_result_amount(amount, deductible_amount, losses, constant_losses):
    intermediate_amount = amount - deductible_amount
    volume_losses = intermediate_amount / 100 * losses
    result_amount = intermediate_amount + volume_losses + constant_losses
    return result_amount


def calculation_accrued(result_amount, tariff1, tariff2, tariff3, margin):
    """A function for calculating charges for consumed electricity.
    The formula is derived based on tariffs for rural and urban populations,
    but it is also suitable for other tariffs.
    """
    if result_amount <= 10980:
        accrued = (tariff1 + margin) * result_amount
    elif result_amount <= 14640:
        accrued = ((tariff1 + margin) * 10980) + ((tariff2 + margin) * (result_amount - 10980))
    else:
        accrued = ((tariff1 + margin) * 10980) + ((tariff2 + margin) * 3660) + ((tariff3 + margin) * (result_amount - 14640))
    return round(accrued, 2)
