from flask_wtf import FlaskForm
from wtforms import DateField, StringField, SelectField, SubmitField, FloatField, BooleanField, HiddenField
from wtforms.validators import DataRequired, Length, ValidationError
from datetime import date


def fecha_por_debajo_de_hoy(formulario, campo):
    hoy = date.today()
    if campo.data > hoy:
        raise ValidationError('La fecha tiene que ser anterior al día de hoy')

class MovimientosForm(FlaskForm):  # la clase MovimientosForm hereda de FlaskForm
    id = HiddenField()
    fecha = DateField('Fecha', validators=[DataRequired(message='Debe introducir una fecha válida'), fecha_por_debajo_de_hoy])
    concepto = StringField('Concepto', validators=[DataRequired(), Length(min=10)])
    categoria = SelectField('Categoria', choices=[('00', ''), ('SU', 'Supervivencia'), ('OV', 'Ocio/Vicio'),
                            ('CU', 'Cultura'), ('EX', 'Extras')])
    cantidad = FloatField('Cantidad', validators=[DataRequired()])
    esGasto = BooleanField('Es gasto')
    submit = SubmitField('Aceptar')


class FiltraMovimientosForm(FlaskForm):
    fechaDesde = DateField('Desde', validators=[fecha_por_debajo_de_hoy], default=date(1,1,1))  
    # pasamos la función fecha_por_debajo_de_hoy pero
    # no la ejecutamos, por eso no le ponemos los ()
    fechaHasta = DateField('Hasta', validators=[fecha_por_debajo_de_hoy], default=date.today())
    texto = StringField('Concepto')
    submit = SubmitField('Filtrar')
