
tofile <- function(p, outFile="", type="") {
    if (outFile == "") {
        print (p)
    } else {
        if (type == "pdf" || type == "") {
            pdf(outFile, paper="a4")
            print(p)
            dev.off()
        } else if (type == "jpg") {
            jpeg(outFile, width=8,height=6,units="in",res=400, pointsize=1)
            print(p)
            dev.off()
        } else if (type == "png") {
            png(outFile, width=8,height=6,units="in",res=400, pointsize=1)
            print(p)
            dev.off()
        }
    }
}

