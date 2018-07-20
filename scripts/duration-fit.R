
##	directory with data files
#dataDir <- './hour'
dataDir <- './day'
#dataDir <- './week'


##	get list of data files in directory
( files <- list.files(dataDir) )

nFiles <- length(files)

## summary matrix
# - growth phase information 'g'
# - decline phase information 'd'
ans <- c('fileName','splitIndex','gLength','dLength')
dataSum <- as.data.frame(matrix(ncol=length(ans), nrow=nFiles))
colnames(dataSum) <- ans

## process data
for (i in 1:length(files)) {

	##	data
	bob <- read.csv(paste(dataDir,files[i],sep='/'), stringsAsFactors=FALSE, strip.white=TRUE, blank.lines.skip=TRUE) 
	colnames(bob) <- c('duration.increment','peers.total','seeds.total','new.peers','new.seeds','duration.string')

	##	get peak seeds
	splitIndex <- which.max(bob$seeds.total)
	
	##	split growth phase from decline phase
	gData <- bob[(0:splitIndex),]
	dData <- bob[(splitIndex:nrow(bob)),]

	##	length of series
	gLength <- nrow(gData)
	dLength <- nrow(dData)
	
	##	summary information
	dataSum[i,'fileName'] <- files[i]
	dataSum[i,'splitIndex'] <- splitIndex
	dataSum[i,'gLength'] <- gLength
	dataSum[i,'dLength'] <- dLength
	
	## log/reset series start
	gData$log2Seeds <- log2(gData$seeds.total)
	gData$peakSeeds <- gData$duration.increment - min(gData$duration.increment)

	if (gLength > 3) {
		gFit <- lm(log2Seeds ~ peakSeeds, data=gData)
		dataSum[i,'g.r2'] <- summary(gFit)$adj.r.squared
		dataSum[i,'g.int.est'] <- summary(gFit)$coefficients[1,1]
		dataSum[i,'g.int.unc'] <- summary(gFit)$coefficients[1,2]
		dataSum[i,'g.slo.est'] <- summary(gFit)$coefficients[2,1]
		dataSum[i,'g.slo.unc'] <- summary(gFit)$coefficients[2,2]		
	}

	## log/reset series start
	dData$log2Seeds <- log2(dData$seeds.total)
	dData$peakSeeds <- dData$duration.increment - min(dData$duration.increment)
	
	if (dLength > 3) {
		dFit <- lm(log2Seeds ~ peakSeeds, data=dData)
		dataSum[i,'d.r2'] <- summary(dFit)$adj.r.squared
		dataSum[i,'d.int.est'] <- summary(dFit)$coefficients[1,1]
		dataSum[i,'d.int.unc'] <- summary(dFit)$coefficients[1,2]
		dataSum[i,'d.slo.est'] <- summary(dFit)$coefficients[2,1]
		dataSum[i,'d.slo.unc'] <- summary(dFit)$coefficients[2,2]
	}
}

dataSum$fileName <- as.factor(dataSum$fileName)

par(mar=c(14,5,1,1))
plot((dataSum$fileName),dataSum$d.slo.est, ylim=range(c(dataSum$d.slo.est+ dataSum$d.slo.unc, dataSum$d.slo.est-dataSum$d.slo.unc)), las=3, ylab='exponential slope')
segments((1:nFiles),(dataSum$d.slo.est+dataSum$d.slo.unc),(1:nFiles), (dataSum$d.slo.est-dataSum$d.slo.unc), lwd=3)

i <- 2

plot(bob$duration.increment,log(bob$peers.total))
plot(bob$duration.increment, log(bob$seeds.total))

aa <- lm(log(bob$seeds.total) ~ bob$duration.increment)
plot(aa)