# Auto generated configuration file
# using:
# Revision: 1.19
# Source: /local/reps/CMSSW/CMSSW/Configuration/Applications/python/ConfigBuilder.py,v
# with command line options: step3 --conditions auto:phase1_2021_realistic --pileup_input das:/RelValMinBias_13/CMSSW_10_6_0_pre3-105X_postLS2_realistic_v6-v1/GEN-SIM -n 10 --era Run3 --eventcontent RECOSIM,DQM -s RAW2DIGI:RawToDigi_pixelOnly,RECO:reconstruction_pixelTrackingOnly,VALIDATION:@pixelTrackingOnlyValidation,DQM:@pixelTrackingOnlyDQM --datatier GEN-SIM-RECO,DQMIO --geometry DB:Extended --pileup Run3_Flat55To75_PoissonOOTPU --filein file:step2_1.root --fileout file:step3.root --procModifiers gpu --runUnscheduled
import FWCore.ParameterSet.Config as cms

from Configuration.Eras.Era_Run3_cff import Run3
from Configuration.ProcessModifiers.gpu_cff import gpu
from FWCore.ParameterSet.VarParsing import VarParsing

import sys
process = cms.Process('Patatrack',Run3,gpu)
from file_list import *
# import of standard configurations
process.load('Configuration.StandardSequences.Services_cff')
process.load('SimGeneral.HepPDTESSource.pythiapdt_cfi')
process.load('FWCore.MessageService.MessageLogger_cfi')
process.load('HeterogeneousCore.CUDAServices.CUDAService_cfi')
process.load('Configuration.EventContent.EventContent_cff')
process.load('SimGeneral.MixingModule.mix_Run3_Flat55To75_PoissonOOTPU_cfi')
process.load('Configuration.StandardSequences.GeometryRecoDB_cff')
process.load('Configuration.StandardSequences.MagneticField_cff')
process.load('Configuration.StandardSequences.RawToDigi_cff')
process.load('Configuration.StandardSequences.Reconstruction_cff')
process.load('Configuration.StandardSequences.Validation_cff')
process.load('DQMServices.Core.DQMStoreNonLegacy_cff')
process.load('DQMOffline.Configuration.DQMOfflineMC_cff')
process.load('Configuration.StandardSequences.FrontierConditions_GlobalTag_cff')

options = VarParsing ('analysis')
options.register ('skipFiles',0,VarParsing.multiplicity.singleton,VarParsing.varType.int,"Skip Files")
options.register ('numFiles',100,VarParsing.multiplicity.singleton,VarParsing.varType.int,"Num Files")
# options.register ('maxEvents',5000,VarParsing.multiplicity.singleton,VarParsing.varType.int,"Num Events")
options.register ('fileName',"step3",VarParsing.multiplicity.singleton,VarParsing.varType.string,"File Name")
options.parseArguments()

process.maxEvents = cms.untracked.PSet(
    input = cms.untracked.int32(-1)
)

if options.skipFiles>len(file_list):
    print("Skipping all files in the list.")
    print("Returning.")
    print("Bye.")
    sys.exit(1)

start = max(0,options.skipFiles)
finish = min(options.numFiles+start,len(file_list))
theList = file_list[start:finish]

print("Processing files from %d to %d (tot=%d)"%(start,finish,len(theList)))

# Input source
process.source = cms.Source("PoolSource",
    fileNames = cms.untracked.vstring(theList),
    inputCommands = cms.untracked.vstring(
        'keep *'),
    secondaryFileNames = cms.untracked.vstring()
)

process.options = cms.untracked.PSet(

)

# Production Info
process.configurationMetadata = cms.untracked.PSet(
    annotation = cms.untracked.string('step3 nevts:10'),
    name = cms.untracked.string('Applications'),
    version = cms.untracked.string('$Revision: 1.19 $')
)

# Output definition

fname = options.fileName + "_" + str(start) + "_" + str(finish)

output = process.FEVTDEBUGHLTEventContent.outputCommands
#output.append("keep *_*tp*_*_*Pata*")
process.FEVTDEBUGHLToutput = cms.OutputModule("PoolOutputModule",
    dataset = cms.untracked.PSet(
        dataTier = cms.untracked.string('GEN-SIM-DIGI-RAW-RECO-HLTDEBUG'),
        filterName = cms.untracked.string('')
    ),
    fileName = cms.untracked.string('file:' + fname + 'hlt_patatrack.root'),
    outputCommands = output,
    splitLevel = cms.untracked.int32(0)
)

process.DQMoutput = cms.OutputModule("DQMRootOutputModule",
    dataset = cms.untracked.PSet(
        dataTier = cms.untracked.string('DQMIO'),
        filterName = cms.untracked.string('')
    ),
    fileName = cms.untracked.string('file:' + fname + 'hlt_patatrack_inDQM.root'),
    outputCommands = process.DQMEventContent.outputCommands,
    splitLevel = cms.untracked.int32(0)
)

# Other statements
process.mix.input.fileNames = cms.untracked.vstring(['file:/lustre/cms/store/user/adiflori/MINBIAS106X/037E40A0-0D58-BB43-B32D-34BA65435B27.root',
'file:/lustre/cms/store/user/adiflori/MINBIAS106X/38806EE1-709B-404D-8744-485FFFEBCE77.root',
'file:/lustre/cms/store/user/adiflori/MINBIAS106X/3EC307BB-54BA-2443-90EA-FD926B91FA9A.root',
'file:/lustre/cms/store/user/adiflori/MINBIAS106X/41F88CCA-3E51-5441-B284-DF542FCEB6E5.root',
'file:/lustre/cms/store/user/adiflori/MINBIAS106X/644621DF-62ED-E34F-A25A-F9871DC2612C.root',
'file:/lustre/cms/store/user/adiflori/MINBIAS106X/6CF4F679-7EA3-0F42-841E-66DD4DD05943.root'])

#process.mix.input.fileNames = cms.untracked.vstring(['/store/relval/CMSSW_10_6_0_pre3/RelValMinBias_13/GEN-SIM/105X_postLS2_realistic_v6-v1/10000/38806EE1-709B-404D-8744-485FFFEBCE77.root', '/store/relval/CMSSW_10_6_0_pre3/RelValMinBias_13/GEN-SIM/105X_postLS2_realistic_v6-v1/10000/6CF4F679-7EA3-0F42-841E-66DD4DD05943.root', '/store/relval/CMSSW_10_6_0_pre3/RelValMinBias_13/GEN-SIM/105X_postLS2_realistic_v6-v1/10000/037E40A0-0D58-BB43-B32D-34BA65435B27.root', '/store/relval/CMSSW_10_6_0_pre3/RelValMinBias_13/GEN-SIM/105X_postLS2_realistic_v6-v1/10000/644621DF-62ED-E34F-A25A-F9871DC2612C.root', '/store/relval/CMSSW_10_6_0_pre3/RelValMinBias_13/GEN-SIM/105X_postLS2_realistic_v6-v1/10000/41F88CCA-3E51-5441-B284-DF542FCEB6E5.root', '/store/relval/CMSSW_10_6_0_pre3/RelValMinBias_13/GEN-SIM/105X_postLS2_realistic_v6-v1/10000/3EC307BB-54BA-2443-90EA-FD926B91FA9A.root'])
process.mix.playback = True
process.mix.digitizers = cms.PSet()
for a in process.aliases: delattr(process, a)
process.RandomNumberGeneratorService.restoreStateLabel=cms.untracked.string("randomEngineStateProducer")
from Configuration.AlCa.GlobalTag import GlobalTag
process.GlobalTag = GlobalTag(process.GlobalTag, 'auto:phase1_2021_realistic', '')

# Path and EndPath definitions
process.raw2digi_step = cms.Path(process.RawToDigi_pixelOnly)
process.reconstruction_step = cms.Path(process.reconstruction_pixelTrackingOnly)
process.prevalidation_step = cms.Path(process.globalPrevalidationPixelTrackingOnly)
process.validation_step = cms.EndPath(process.globalValidationPixelTrackingOnly)
process.dqmoffline_step = cms.EndPath(process.DQMOfflinePixelTracking)
process.dqmofflineOnPAT_step = cms.EndPath(process.PostDQMOffline)
#process.RECOSIMoutput_step = cms.EndPath(process.RECOSIMoutput)
process.DQMoutput_step = cms.EndPath(process.DQMoutput)
process.FEVTDEBUGHLToutput_step = cms.EndPath(process.FEVTDEBUGHLToutput)

# Schedule definition
process.schedule = cms.Schedule(process.raw2digi_step,process.reconstruction_step,process.prevalidation_step,process.validation_step,process.dqmoffline_step,process.dqmofflineOnPAT_step,process.FEVTDEBUGHLToutput_step,process.DQMoutput_step)
from PhysicsTools.PatAlgos.tools.helpers import associatePatAlgosToolsTask
associatePatAlgosToolsTask(process)

# customisation of the process.
process.MessageLogger.cerr.FwkReport.reportEvery = 100
# Automatic addition of the customisation function from SimGeneral.MixingModule.fullMixCustomize_cff
from SimGeneral.MixingModule.fullMixCustomize_cff import setCrossingFrameOn

#call to customisation function setCrossingFrameOn imported from SimGeneral.MixingModule.fullMixCustomize_cff
process = setCrossingFrameOn(process)

# End of customisation functions
#do not add changes to your config after this point (unless you know what you are doing)
#from FWCore.ParameterSet.Utilities import convertToUnscheduled
#process=convertToUnscheduled(process)

process.options.numberOfThreads=cms.untracked.uint32(2)
process.options.numberOfStreams=cms.untracked.uint32(2)
process.options.numberOfConcurrentLuminosityBlocks=cms.untracked.uint32(2)

#process.Timing = cms.Service("Timing",
#  summaryOnly = cms.untracked.bool(False),
#  useJobReport = cms.untracked.bool(True)
#)

# Customisation from command line

#Have logErrorHarvester wait for the same EDProducers to finish as those providing data for the OutputModule
from FWCore.Modules.logErrorHarvester_cff import customiseLogErrorHarvesterUsingOutputCommands
process = customiseLogErrorHarvesterUsingOutputCommands(process)

# Add early deletion of temporary data products to reduce peak memory need
from Configuration.StandardSequences.earlyDeleteSettings_cff import customiseEarlyDelete
process = customiseEarlyDelete(process)
# End adding early deletion
