"""
Model exported as python.
Name : ICA 100-40 FRZ
Group : 
With QGIS : 33410
"""

from qgis.core import QgsProcessing
from qgis.core import QgsProcessingAlgorithm
from qgis.core import QgsProcessingMultiStepFeedback
from qgis.core import QgsProcessingParameterMapLayer
from qgis.core import QgsProcessingParameterFeatureSink
from qgis.core import QgsProcessingParameterDefinition
from qgis.core import QgsProperty
import processing


class Ica10040Frz(QgsProcessingAlgorithm):

    def initAlgorithm(self, config=None):
        param = QgsProcessingParameterMapLayer('camada_de_linha_pista_aerodromo', 'Camada de linha (Pista Aerodromo)', defaultValue=None, types=[QgsProcessing.TypeVectorLine])
        param.setFlags(param.flags() | QgsProcessingParameterDefinition.FlagAdvanced)
        self.addParameter(param)
        self.addParameter(QgsProcessingParameterFeatureSink('Resultado', 'Resultado', type=QgsProcessing.TypeVectorAnyGeometry, createByDefault=True, supportsAppend=True, defaultValue=None))

    def processAlgorithm(self, parameters, context, model_feedback):
        # Use a multi-step feedback, so that individual child algorithm progress reports are adjusted for the
        # overall progress through the model
        feedback = QgsProcessingMultiStepFeedback(29, model_feedback)
        results = {}
        outputs = {}

        # Extrair vértices
        alg_params = {
            'INPUT': parameters['camada_de_linha_pista_aerodromo'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['ExtrairVrtices'] = processing.run('native:extractvertices', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(1)
        if feedback.isCanceled():
            return {}

        # Calculadora de campo
        alg_params = {
            'FIELD_LENGTH': 0,
            'FIELD_NAME': 'angle',
            'FIELD_PRECISION': 0,
            'FIELD_TYPE': 0,  # Decimal (double)
            'FORMULA': 'if(vertex_index=0,angle-180,angle)',
            'INPUT': outputs['ExtrairVrtices']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['CalculadoraDeCampo'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(2)
        if feedback.isCanceled():
            return {}

        # Criar buffer em cunha (300FT)
        alg_params = {
            'AZIMUTH': QgsProperty.fromExpression('angle'),
            'INNER_RADIUS': 5400,
            'INPUT': outputs['CalculadoraDeCampo']['OUTPUT'],
            'OUTER_RADIUS': 6320,
            'WIDTH': 40,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['CriarBufferEmCunha300ft'] = processing.run('native:wedgebuffers', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(3)
        if feedback.isCanceled():
            return {}

        # Buffer 100 ft
        alg_params = {
            'DISSOLVE': False,
            'DISTANCE': 2350,
            'END_CAP_STYLE': 0,  # Arredondado
            'INPUT': parameters['camada_de_linha_pista_aerodromo'],
            'JOIN_STYLE': 0,  # Arredondado
            'MITER_LIMIT': 2,
            'SEGMENTS': 20,
            'SEPARATE_DISJOINT': False,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Buffer100Ft'] = processing.run('native:buffer', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(4)
        if feedback.isCanceled():
            return {}

        # Buffer 200ft
        alg_params = {
            'DISSOLVE': False,
            'DISTANCE': 2960,
            'END_CAP_STYLE': 0,  # Arredondado
            'INPUT': parameters['camada_de_linha_pista_aerodromo'],
            'JOIN_STYLE': 0,  # Arredondado
            'MITER_LIMIT': 2,
            'SEGMENTS': 20,
            'SEPARATE_DISJOINT': False,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Buffer200ft'] = processing.run('native:buffer', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(5)
        if feedback.isCanceled():
            return {}

        # Buffer FRZ
        alg_params = {
            'DISSOLVE': False,
            'DISTANCE': 1740,
            'END_CAP_STYLE': 0,  # Arredondado
            'INPUT': parameters['camada_de_linha_pista_aerodromo'],
            'JOIN_STYLE': 0,  # Arredondado
            'MITER_LIMIT': 2,
            'SEGMENTS': 20,
            'SEPARATE_DISJOINT': False,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['BufferFrz'] = processing.run('native:buffer', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(6)
        if feedback.isCanceled():
            return {}

        # Criar buffer em cunha (FRZ)
        alg_params = {
            'AZIMUTH': QgsProperty.fromExpression('angle'),
            'INNER_RADIUS': 0,
            'INPUT': outputs['CalculadoraDeCampo']['OUTPUT'],
            'OUTER_RADIUS': 3550,
            'WIDTH': 40,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['CriarBufferEmCunhaFrz'] = processing.run('native:wedgebuffers', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(7)
        if feedback.isCanceled():
            return {}

        # Buffer 300 ft
        alg_params = {
            'DISSOLVE': False,
            'DISTANCE': 3570,
            'END_CAP_STYLE': 0,  # Arredondado
            'INPUT': parameters['camada_de_linha_pista_aerodromo'],
            'JOIN_STYLE': 0,  # Arredondado
            'MITER_LIMIT': 2,
            'SEGMENTS': 20,
            'SEPARATE_DISJOINT': False,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Buffer300Ft'] = processing.run('native:buffer', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(8)
        if feedback.isCanceled():
            return {}

        # Criar buffer em cunha (100FT)
        alg_params = {
            'AZIMUTH': QgsProperty.fromExpression('angle'),
            'INNER_RADIUS': 3550,
            'INPUT': outputs['CalculadoraDeCampo']['OUTPUT'],
            'OUTER_RADIUS': 4480,
            'WIDTH': 40,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['CriarBufferEmCunha100ft'] = processing.run('native:wedgebuffers', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(9)
        if feedback.isCanceled():
            return {}

        # Calculadora de campo buf 300 ft
        alg_params = {
            'FIELD_LENGTH': 0,
            'FIELD_NAME': 'tipo',
            'FIELD_PRECISION': 0,
            'FIELD_TYPE': 2,  # Texto (string)
            'FORMULA': "'<300 ft'",
            'INPUT': outputs['CriarBufferEmCunha300ft']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['CalculadoraDeCampoBuf300Ft'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(10)
        if feedback.isCanceled():
            return {}

        # Criar buffer em cunha (200FT)
        alg_params = {
            'AZIMUTH': QgsProperty.fromExpression('angle'),
            'INNER_RADIUS': 4480,
            'INPUT': outputs['CalculadoraDeCampo']['OUTPUT'],
            'OUTER_RADIUS': 5400,
            'WIDTH': 40,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['CriarBufferEmCunha200ft'] = processing.run('native:wedgebuffers', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(11)
        if feedback.isCanceled():
            return {}

        # Diferença 300ft
        alg_params = {
            'GRID_SIZE': None,
            'INPUT': outputs['Buffer300Ft']['OUTPUT'],
            'OVERLAY': outputs['Buffer200ft']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Diferena300ft'] = processing.run('native:difference', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(12)
        if feedback.isCanceled():
            return {}

        # União FRZ
        alg_params = {
            'GRID_SIZE': None,
            'INPUT': outputs['BufferFrz']['OUTPUT'],
            'OVERLAY': outputs['CriarBufferEmCunhaFrz']['OUTPUT'],
            'OVERLAY_FIELDS_PREFIX': '',
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['UnioFrz'] = processing.run('native:union', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(13)
        if feedback.isCanceled():
            return {}

        # Diferença 200ft
        alg_params = {
            'GRID_SIZE': None,
            'INPUT': outputs['Buffer200ft']['OUTPUT'],
            'OVERLAY': outputs['Buffer100Ft']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Diferena200ft'] = processing.run('native:difference', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(14)
        if feedback.isCanceled():
            return {}

        # Dissolver FRZ
        alg_params = {
            'FIELD': [''],
            'INPUT': outputs['UnioFrz']['OUTPUT'],
            'SEPARATE_DISJOINT': False,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['DissolverFrz'] = processing.run('native:dissolve', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(15)
        if feedback.isCanceled():
            return {}

        # Diferença 200ft - frz
        alg_params = {
            'GRID_SIZE': None,
            'INPUT': outputs['Diferena200ft']['OUTPUT'],
            'OVERLAY': outputs['DissolverFrz']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Diferena200ftFrz'] = processing.run('native:difference', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(16)
        if feedback.isCanceled():
            return {}

        # Calculadora de campo buf 100 ft
        alg_params = {
            'FIELD_LENGTH': 0,
            'FIELD_NAME': 'tipo',
            'FIELD_PRECISION': 0,
            'FIELD_TYPE': 2,  # Texto (string)
            'FORMULA': "'<100 ft'",
            'INPUT': outputs['CriarBufferEmCunha100ft']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['CalculadoraDeCampoBuf100Ft'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(17)
        if feedback.isCanceled():
            return {}

        # Calculadora de campo buf 200 ft
        alg_params = {
            'FIELD_LENGTH': 0,
            'FIELD_NAME': 'tipo',
            'FIELD_PRECISION': 0,
            'FIELD_TYPE': 2,  # Texto (string)
            'FORMULA': "'<200 ft'",
            'INPUT': outputs['CriarBufferEmCunha200ft']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['CalculadoraDeCampoBuf200Ft'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(18)
        if feedback.isCanceled():
            return {}

        # Calculadora de campo DIF 200 ft - frz
        alg_params = {
            'FIELD_LENGTH': 0,
            'FIELD_NAME': 'tipo',
            'FIELD_PRECISION': 0,
            'FIELD_TYPE': 2,  # Texto (string)
            'FORMULA': "'<200 ft'",
            'INPUT': outputs['Diferena200ftFrz']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['CalculadoraDeCampoDif200FtFrz'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(19)
        if feedback.isCanceled():
            return {}

        # Diferença 300ft - frz
        alg_params = {
            'GRID_SIZE': None,
            'INPUT': outputs['Diferena300ft']['OUTPUT'],
            'OVERLAY': outputs['DissolverFrz']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Diferena300ftFrz'] = processing.run('native:difference', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(20)
        if feedback.isCanceled():
            return {}

        # Calculadora de campo DIF 300 ft - frz
        alg_params = {
            'FIELD_LENGTH': 0,
            'FIELD_NAME': 'tipo',
            'FIELD_PRECISION': 0,
            'FIELD_TYPE': 2,  # Texto (string)
            'FORMULA': "'<300 ft'",
            'INPUT': outputs['Diferena300ftFrz']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['CalculadoraDeCampoDif300FtFrz'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(21)
        if feedback.isCanceled():
            return {}

        # Calculadora de campo dissolv FRZ
        alg_params = {
            'FIELD_LENGTH': 0,
            'FIELD_NAME': 'tipo',
            'FIELD_PRECISION': 0,
            'FIELD_TYPE': 2,  # Texto (string)
            'FORMULA': "'FRZ'",
            'INPUT': outputs['DissolverFrz']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['CalculadoraDeCampoDissolvFrz'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(22)
        if feedback.isCanceled():
            return {}

        # Diferença 100ft
        alg_params = {
            'GRID_SIZE': None,
            'INPUT': outputs['Buffer100Ft']['OUTPUT'],
            'OVERLAY': outputs['DissolverFrz']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Diferena100ft'] = processing.run('native:difference', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(23)
        if feedback.isCanceled():
            return {}

        # Diferença 100ft - frz
        alg_params = {
            'GRID_SIZE': None,
            'INPUT': outputs['Diferena100ft']['OUTPUT'],
            'OVERLAY': outputs['DissolverFrz']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['Diferena100ftFrz'] = processing.run('native:difference', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(24)
        if feedback.isCanceled():
            return {}

        # Calculadora de campo DIF 100 ft - frz
        alg_params = {
            'FIELD_LENGTH': 0,
            'FIELD_NAME': 'tipo',
            'FIELD_PRECISION': 0,
            'FIELD_TYPE': 2,  # Texto (string)
            'FORMULA': "'<100 ft'",
            'INPUT': outputs['Diferena100ftFrz']['OUTPUT'],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['CalculadoraDeCampoDif100FtFrz'] = processing.run('native:fieldcalculator', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(25)
        if feedback.isCanceled():
            return {}

        # Mesclar camadas vetoriais
        alg_params = {
            'CRS': None,
            'LAYERS': [outputs['CalculadoraDeCampoBuf100Ft']['OUTPUT'],outputs['CalculadoraDeCampoBuf200Ft']['OUTPUT'],outputs['CalculadoraDeCampoBuf300Ft']['OUTPUT'],outputs['CalculadoraDeCampoDissolvFrz']['OUTPUT'],outputs['CalculadoraDeCampoDif100FtFrz']['OUTPUT'],outputs['CalculadoraDeCampoDif200FtFrz']['OUTPUT'],outputs['CalculadoraDeCampoDif300FtFrz']['OUTPUT']],
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['MesclarCamadasVetoriais'] = processing.run('native:mergevectorlayers', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(26)
        if feedback.isCanceled():
            return {}

        # Adicionar campo de autoincremento
        alg_params = {
            'FIELD_NAME': 'AUTO',
            'GROUP_FIELDS': [''],
            'INPUT': outputs['MesclarCamadasVetoriais']['OUTPUT'],
            'MODULUS': 0,
            'SORT_ASCENDING': True,
            'SORT_EXPRESSION': '',
            'SORT_NULLS_FIRST': False,
            'START': 0,
            'OUTPUT': QgsProcessing.TEMPORARY_OUTPUT
        }
        outputs['AdicionarCampoDeAutoincremento'] = processing.run('native:addautoincrementalfield', alg_params, context=context, feedback=feedback, is_child_algorithm=True)

        feedback.setCurrentStep(27)
        if feedback.isCanceled():
            return {}

        # Editar campos
        alg_params = {
            'FIELDS_MAPPING': [{'alias': '','comment': '','expression': '"AUTO"','length': 0,'name': 'AUTO','precision': 0,'sub_type': 0,'type': 4,'type_name': 'int8'},{'alias': '','comment': '','expression': '"nome"','length': 255,'name': 'nome','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'},{'alias': '','comment': '','expression': '"tipo"','length': 0,'name': 'tipo','precision': 0,'sub_type': 0,'type': 10,'type_name': 'text'}],
            'INPUT': outputs['AdicionarCampoDeAutoincremento']['OUTPUT'],
            'OUTPUT': parameters['Resultado']
        }
        outputs['EditarCampos'] = processing.run('native:refactorfields', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        results['Resultado'] = outputs['EditarCampos']['OUTPUT']

        feedback.setCurrentStep(28)
        if feedback.isCanceled():
            return {}

        # configurar estilo de camada
        alg_params = {
            'INPUT': outputs['EditarCampos']['OUTPUT'],
            'STYLE': 'C:\\Users\\limab\\AppData\\Roaming\\QGIS\\QGIS3\\profiles\\default\\processing\\models\\estilo_ica_100_40.qml'
        }
        outputs['ConfigurarEstiloDeCamada'] = processing.run('native:setlayerstyle', alg_params, context=context, feedback=feedback, is_child_algorithm=True)
        return results

    def name(self):
        return 'ICA 100-40 FRZ'

    def displayName(self):
        return 'ICA 100-40 FRZ'

    def group(self):
        return ''

    def groupId(self):
        return ''

    def createInstance(self):
        return Ica10040Frz()
