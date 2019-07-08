import FWCore.ParameterSet.Config as cms

# customisation for offloading to GPUs, common parts
def customise_gpu_common(process):

    # Services

    process.CUDAService = cms.Service("CUDAService",
        allocator = cms.untracked.PSet(
            binGrowth = cms.untracked.uint32(8),
            debug = cms.untracked.bool(False),
            devicePreallocate = cms.untracked.vuint32(),
            enabled = cms.untracked.bool(True),
            hostPreallocate = cms.untracked.vuint32(),
            maxBin = cms.untracked.uint32(9),
            maxCachedBytes = cms.untracked.uint32(0),
            maxCachedFraction = cms.untracked.double(0.8),
            minBin = cms.untracked.uint32(1)
        ),
        enabled = cms.untracked.bool(True),
        limits = cms.untracked.PSet(
            cudaLimitDevRuntimePendingLaunchCount = cms.untracked.int32(-1),
            cudaLimitDevRuntimeSyncDepth = cms.untracked.int32(-1),
            cudaLimitMallocHeapSize = cms.untracked.int32(-1),
            cudaLimitPrintfFifoSize = cms.untracked.int32(-1),
            cudaLimitStackSize = cms.untracked.int32(-1)
        )
    )

    # done
    return process


# customisation for offloading the Pixel local reconstruction to GPUs
def customise_gpu_pixel(process):

    # FIXME replace the Sequences with empty ones to avoid exanding them during the (re)definition of Modules and EDAliases

    process.HLTDoLocalPixelSequence = cms.Sequence()
    process.HLTRecoPixelTracksSequence = cms.Sequence()
    #process.HLTRecopixelvertexingSequence is unchanged


    # Event Setup

    process.siPixelGainCalibrationForHLTGPU = cms.ESProducer("SiPixelGainCalibrationForHLTGPUESProducer",
        appendToDataLabel = cms.string('')
    )

    process.siPixelFedCablingMapGPUWrapper = cms.ESProducer("SiPixelFedCablingMapGPUWrapperESProducer",
        CablingMapLabel = cms.string(''),
        ComponentName = cms.string(''),
        UseQualityInfo = cms.bool(False),
        appendToDataLabel = cms.string('')
    )

    process.PixelCPEFastESProducer = cms.ESProducer("PixelCPEFastESProducer",
        Alpha2Order = cms.bool(True),
        ClusterProbComputationFlag = cms.int32(0),
        ComponentName = cms.string('PixelCPEFast'),
        EdgeClusterErrorX = cms.double(50.0),
        EdgeClusterErrorY = cms.double(85.0),
        LoadTemplatesFromDB = cms.bool(True),
        MagneticFieldRecord = cms.ESInputTag(""),
        TruncatePixelCharge = cms.bool(True),
        UseErrorsFromTemplates = cms.bool(True),
        useLAAlignmentOffsets = cms.bool(False),
        useLAWidthFromDB = cms.bool(True)
    )


    # Modules and EDAliases

    # referenced in process.HLTDoLocalPixelSequence
    process.hltOnlineBeamSpotCUDA = cms.EDProducer("BeamSpotToCUDA",
        src = cms.InputTag("hltOnlineBeamSpot")
    )

    process.siPixelClustersCUDAPreSplitting = cms.EDProducer("SiPixelRawToClusterCUDA",
        CablingMapLabel = cms.string(''),
        IncludeErrors = cms.bool(True),
        InputLabel = cms.InputTag("rawDataCollector"),
        Regions = cms.PSet(
        ),
        UsePilotBlade = cms.bool(False),
        UseQualityInfo = cms.bool(False)
    )

    process.siPixelRecHitsCUDAPreSplitting = cms.EDProducer("SiPixelRecHitCUDA",
        CPE = cms.string('PixelCPEFast'),
        beamSpot = cms.InputTag("hltOnlineBeamSpotCUDA"),
        src = cms.InputTag("siPixelClustersCUDAPreSplitting")
    )

    process.siPixelDigisSoA = cms.EDProducer("SiPixelDigisSoAFromCUDA",
        src = cms.InputTag("siPixelClustersCUDAPreSplitting")
    )

    process.siPixelDigisClustersPreSplitting = cms.EDProducer("SiPixelDigisClustersFromSoA",
        src = cms.InputTag("siPixelDigisSoA")
    )

    process.siPixelDigiErrorsSoA = cms.EDProducer("SiPixelDigiErrorsSoAFromCUDA",
        src = cms.InputTag("siPixelClustersCUDAPreSplitting")
    )

    process.siPixelDigiErrors = cms.EDProducer("SiPixelDigiErrorsFromSoA",
        CablingMapLabel = cms.string(''),
        ErrorList = cms.vint32(29),
        UsePhase1 = cms.bool(True),
        UserErrorList = cms.vint32(40),
        digiErrorSoASrc = cms.InputTag("siPixelDigiErrorsSoA")
    )

    process.hltSiPixelRecHits = cms.EDProducer("SiPixelRecHitFromSOA",
        pixelRecHitSrc = cms.InputTag("siPixelRecHitsCUDAPreSplitting"),
        src = cms.InputTag("siPixelDigisClustersPreSplitting")
    )

    process.hltSiPixelDigis = cms.EDAlias(
        siPixelDigisClustersPreSplitting = cms.VPSet(
            cms.PSet(
                type = cms.string('PixelDigiedmDetSetVector')
            )
        ),
        siPixelDigiErrors = cms.VPSet(
            cms.PSet(
                type = cms.string('DetIdedmEDCollection')
            ),
            cms.PSet(
                type = cms.string('SiPixelRawDataErroredmDetSetVector')
            ),
            cms.PSet(
                type = cms.string('PixelFEDChanneledmNewDetSetVector')
            )
        )
    )

    process.hltSiPixelClusters = cms.EDAlias(
        siPixelDigisClustersPreSplitting = cms.VPSet(
            cms.PSet(
                type = cms.string('SiPixelClusteredmNewDetSetVector')
            )
        )
    )

    # referenced in process.HLTRecoPixelTracksSequence
    process.hltPixelTracksHitQuadruplets = cms.EDProducer("CAHitNtupletHeterogeneousEDProducer",
        heterogeneousEnabled_ = cms.untracked.PSet(
            GPUCuda = cms.untracked.bool(True),
            force = cms.untracked.string('')
        ),
        gpuEnableTransfer = cms.bool(True),
        gpuEnableConversion = cms.bool(True),
        CAHardPtCut = cms.double(0),
        CAPhiCut = cms.double(10),
        CAThetaCut = cms.double(0.00125),
        CAThetaCutBarrel = cms.double(0.00200000009499),
        CAThetaCutForward = cms.double(0.00300000002608),
        dcaCutInnerTriplet = cms.double(0.15000000596),
        dcaCutOuterTriplet = cms.double(0.25),
        doClusterCut = cms.bool(True),
        doPhiCut = cms.bool(True),
        doZCut = cms.bool(True),
        earlyFishbone = cms.bool(False),
        fillStatistics = cms.bool(False),
        fit5as4 = cms.bool(True),
        hardCurvCut = cms.double(0.0328407224959),
        idealConditions = cms.bool(True),
        lateFishbone = cms.bool(True),
        minHitsPerNtuplet = cms.uint32(4),
        pixelRecHitLegacySrc = cms.InputTag("hltSiPixelRecHits"),
        pixelRecHitSrc = cms.InputTag("siPixelRecHitsCUDAPreSplitting"),
        ptmin = cms.double(0.899999976158),
        trackingRegions = cms.InputTag("hltPixelTracksTrackingRegions"),
        useRiemannFit = cms.bool(False)
    )

    process.hltPixelTracks = cms.EDProducer("PixelTrackProducerFromCUDA",
        heterogeneousEnabled_ = cms.untracked.PSet(
            GPUCuda = cms.untracked.bool(True),
            force = cms.untracked.string('')
        ),
        gpuEnableConversion = cms.bool(True),
        beamSpot = cms.InputTag("hltOnlineBeamSpot"),
        src = cms.InputTag("hltPixelTracksHitQuadruplets")
    )

    # referenced in process.HLTRecopixelvertexingSequence
    process.hltPixelVertices = cms.EDProducer("PixelVertexHeterogeneousProducer",
        heterogeneousEnabled_ = cms.untracked.PSet(
            GPUCuda = cms.untracked.bool(True),
            force = cms.untracked.string('')
        ),
        gpuEnableTransfer = cms.bool(True),
        gpuEnableConversion = cms.bool(True),
        PtMin = cms.double(0.5),
        TrackCollection = cms.InputTag("hltPixelTracks"),
        beamSpot = cms.InputTag("hltOnlineBeamSpot"),
        chi2max = cms.double(9),
        eps = cms.double(0.07),
        errmax = cms.double(0.01),
        minT = cms.int32(2),
        src = cms.InputTag("hltPixelTracksHitQuadruplets"),
        useDBSCAN = cms.bool(False),
        useDensity = cms.bool(True),
        useIterative = cms.bool(False)
    )


    # Sequences

    process.HLTDoLocalPixelSequence = cms.Sequence(
          process.hltOnlineBeamSpotCUDA                     # transfer the beamspot to the gpu
        + process.siPixelClustersCUDAPreSplitting           # digis and clusters on gpu
        + process.siPixelRecHitsCUDAPreSplitting            # rechits on gpu
        + process.siPixelDigisSoA                           # copy to host
        + process.siPixelDigisClustersPreSplitting          # convert to legacy
        + process.siPixelDigiErrorsSoA                      # copy to host
        + process.siPixelDigiErrors                         # convert to legacy
        # process.hltSiPixelDigis                           # replaced by an alias
        # process.hltSiPixelClusters                        # replaced by an alias
        + process.hltSiPixelClustersCache                   # not used here, kept for compatibility with legacy sequences
        + process.hltSiPixelRecHits)                        # convert to legacy

    process.HLTRecoPixelTracksSequence = cms.Sequence(
          process.hltPixelTracksFitter                      # not used here, kept for compatibility with legacy sequences
        + process.hltPixelTracksFilter                      # not used here, kept for compatibility with legacy sequences
        + process.hltPixelTracksTrackingRegions             #
        + process.hltPixelTracksHitQuadruplets              # pixel ntuplets on gpu, with transfer and conversion to legacy
        + process.hltPixelTracks)                           # pixel tracks on gpu, with transfer and conversion to legacy

    #process.HLTRecopixelvertexingSequence is unchanged


    # done
    return process


# customisation for offloading to GPUs
def customise_gpu(process):
    process = customise_gpu_common(process)
    process = customise_gpu_pixel(process)
    return process
