options(tz="CA")
options(tikzMetricPackages = c("\\usepackage{preview}", "\\usepackage[utf8]{inputenc}","\\usepackage[T1]{fontenc}", "\\usetikzlibrary{calc}", "\\usepackage{amssymb}"))


# success rate versus ring size
res_fig <- read.csv("../../results/changes_shape_passive_attack_ring.csv")
res_fig <- data.table(res_fig)

heuristic <- res_fig[, .(ring=ring, accuracy=map_unknown_distribution)]
heuristic[, method:="MAP Non Parametric"]

benchmark <- res_fig[, .(ring=ring, accuracy=benchmark)]
benchmark[, method:="Benchmark"]

data <- rbind(benchmark, heuristic)

tikz(file = "..\\figure_ringsize.tex", width = 2.75, height = 2.75)

plt1 <- ggplot(data)
plt1 <- plt1 + geom_point(aes(x=ring, y=accuracy, color=method, shape=method),  show.legend=F)
plt1 <- plt1 + geom_line(aes(x=ring, y=accuracy, color=method) )            
plt1 <- plt1 + theme(panel.grid.major = element_line(colour = "gray"),
                     panel.background = element_blank(), axis.line = element_line(colour = "black"))
plt1 <- plt1 +  scale_color_manual(values=c("MAP Non Parametric"="red", "Benchmark"="blue"), 
                                   labels=c("MAP Non Parametric", "Random Guess"), 
                                   breaks=c("MAP Non Parametric", "Benchmark"))
plt1 <- plt1 + scale_x_continuous(limits = c(5, 15))
plt1 <- plt1 + scale_y_continuous(limits = c(0, 0.3))
#plt1 <- plt1 + theme(legend.position="bottom")

plt1 <- plt1 + theme(text = element_text(size=17))
plt1 <- plt1  + theme(legend.position = c(0.7, 0.9), legend.text=element_text(size=6))
plt1 <- plt1 + theme(legend.key=element_blank(),
                     legend.title=element_blank(),
                     legend.box="vertical")
plt1 <- plt1 + theme(text = element_text(size=10))
plt1 <- plt1 + guides(color=guide_legend(
  keywidth=0.15,
  keyheight=0.15,
  default.unit="inch")
)

plt1 <- plt1 + labs(x="Number of mixins", y="Succes rate")
plt1

dev.off()