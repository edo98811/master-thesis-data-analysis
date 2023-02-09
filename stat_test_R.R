SIGNIFICANCE_THRESHOLD <- 0.05


save_csv <- function(base_path, list_line) {
    df <- data.frame()
    
    for (item in list_line) {
        df <- rbind(df, data.frame(mann_whitney_p_value = item$mann_whitney$p_value,
                                mann_whitney_outcome = item$mann_whitney$outcome,
                                mann_whitney_message = item$mann_whitney$result,
                                t_test_p_value = item$t_test$p_value,
                                t_test_outcome = item$t_test$outcome,
                                t_test_message = item$t_test$result,
                                significance_threshold_used = SIGNIFICANCE_THRESHOLD,
                                row.names = item$name))
    }
    
    write.csv(df, file = paste(base_path, "test_results_R.csv", sep=""))
}

# i think i can delete this
get_column <- function(column_to_compare, df1, df2) {

    if (is.numeric(column_to_compare)) {
        a = df1[,column_to_compare]
        b = df2[,column_to_compare]
    }
    if (is.character(column_to_compare)) {
        a = df1[,column_to_compare]
        b = df2[,column_to_compare]
    }

return(list(a=a, b=b))
}

mann_whitney <- function(base_path, filename1, filename2, column_to_compare) {
    library(dplyr)
    library(stats)
    
    df1 = read.csv(paste(base_path, filename1, sep=""))
    df2 = read.csv(paste(base_path, filename2, sep=""))
    
    df1 = df1[df1$subjects %in% df2$subjects, ]

    # result = get_column(column_to_compare, df1, df2)
    # a = result$a
    # b = result$b
    a = df1[column_to_compare]
    b = df2[column_to_compare]
    p_value = NA
    
    if (any(is.na(c(a,b)))) {
        return(c("result could not be computed", "NaN", "NaN"))
    }
    
    t_stat = wilcox.test(a, b)$statistic
    p_value = wilcox.test(a, b)$p.value

    if (p_value == NA){
        result = paste("result could not be computed")
        outcome = -1    
    } else if (p_value > 0.05) {
        result = paste("p-value:", p_value, "- null hypothesis cannot be rejected, the datasets have the same distribution")
        outcome = 0
    } else {
        result = paste("p-value:", p_value, "- null hypothesis rejected, the datasets have a different distribution")
        outcome = 1
    }
    
  return(list(result=result, p_value=p_value, outcome=outcome))
}

t_test <- function(base_path, filename1, filename2, column_to_compare) {
    df1 = read.csv(paste(base_path, filename1, sep=""))
    df2 = read.csv(paste(base_path, filename2, sep=""))
    
    df1 = df1[df1$subjects %in% df2$subjects,]

    # result = get_column(column_to_compare, df1, df2)
    # a = result$a
    # b = result$b
    a = df1[column_to_compare]
    b = df2[column_to_compare]
    p_value = NA
    
    if (any(is.na(c(a, b)))) {
        print("could not compute")
        return(list(result="result could not be computed", p_value="NaN", outcome="NaN"))
    }
    
    t.test = t.test(a, b)
    p_value = t.test$p.value

    if (p_value == NA){
        result = paste("result could not be computed")
        outcome = -1    
    } else if (p_value > 0.05) {
        result = paste("p-value:", p_value, "- null hypothesis cannot be rejected, means are statistically equal")
        outcome = 0
    } else {
        result = paste("p-value:", p_value, "- null hypothesis rejected, means are not statistically equal")
        outcome = 1
  }
  
  return(list(result=result, p_value=p_value, outcome=outcome))
}



stat_test <- function(base_path, filename1, filename2, column_to_compare, r_all) {
    r1 = mann_whitney(base_path, filename1, filename2, column_to_compare)
    r2 = t_test(base_path, filename1, filename2, column_to_compare)
    
    if (is.numeric(column_to_compare)) {
        df_example = read.csv(paste0(base_path, filename2))
        column_to_compare_name = names(df_example)[column_to_compare + 1] # R is 1-indexed, python is 0-indexed
        
        r_all[[length(r_all) + 1]] = list(name = paste0(filename1, " ", column_to_compare_name), 
                                        mann_whitney = list(result = r1[1], 
                                                            p_value = r1[2], 
                                                            outcome = r1[3]), 
                                        t_test = list(result = r2[1], 
                                                        p_value = r2[2], 
                                                        outcome = r2[3]))
        rm(df_example)
    }
    
    if (is.character(column_to_compare)) {
        r_all[[length(r_all) + 1]] = list(name = paste0(filename1, " ", column_to_compare), 
                                        mann_whitney = list(result = r1[1], 
                                                            p_value = r1[2], 
                                                            outcome = r1[3]), 
                                        t_test = list(result = r2[1], 
                                                        p_value = r2[2], 
                                                        outcome = r2[3]))
    }
}

base_path <- "/media/neuropsycad/disk12t/EdoardoFilippiMasterThesis/"

r_all <- list()

filename1 <- "Stats_Freesurfer/aseg_AD.csv"
filename2 <- "Stats_FastSurfer/aseg_AD.csv"

max_len <- min(ncol(read.csv(paste0(base_path, filename1))), ncol(read.csv(paste0(base_path, filename2))))
for (column_to_compare in 2:(max_len-1)) {
stat_test(base_path, filename1, filename2, column_to_compare, r_all)
}

filename1 <- "Stats_Freesurfer/aseg_healthy.csv"
filename2 <- "Stats_FastSurfer/aseg_healthy.csv"

max_len <- min(ncol(read.csv(paste0(base_path, filename1))), ncol(read.csv(paste0(base_path, filename2))))
for (column_to_compare in 2:(max_len-1)) {
stat_test(base_path, filename1, filename2, column_to_compare, r_all)
}

filename1 <- "Stats_Freesurfer/aparcDKT_left_AD.csv"
filename2 <- "Stats_FastSurfer/aparcDKT_left_AD.csv"

max_len <- min(ncol(read.csv(paste0(base_path, filename1))), ncol(read.csv(paste0(base_path, filename2))))
for (column_to_compare in 2:(max_len-1)) {
stat_test(base_path, filename1, filename2, column_to_compare, r_all)
}

filename1 <- "Stats_Freesurfer/aparcDKT_right_AD.csv"
filename2 <- "Stats_FastSurfer/aparcDKT_right_AD.csv"

max_len <- min(ncol(read.csv(paste0(base_path, filename1))), ncol(read.csv(paste0(base_path, filename2))))
for (column_to_compare in 2:(max_len-1)) {
stat_test(base_path, filename1, filename2, column_to_compare, r_all)
}

filename1 <- "Stats_Freesurfer/aparcDKT_left_healthy.csv"
filename2 <- "Stats_FastSurfer/aparcDKT_left_healthy.csv"

max_len <- min(ncol(read.csv(paste0(base_path, filename1))), ncol(read.csv(paste0(base_path, filename2))))
for (column_to_compare in 2:(max_len-1)) {
stat_test(base_path, filename1, filename2, column_to_compare, r_all)
}

filename1 <- "Stats_Freesurfer/aparcDKT_right_healthy.csv"
filename2 <- "Stats_FastSurfer/aparcDKT_right_healthy.csv"

max_len <- min(ncol(read.csv(file.path(base_path, filename1))), ncol(read.csv(file.path(base_path, filename2))))
for (column_to_compare in 2:(max_len - 1)) {
    stat_test(base_path, filename1, filename2, column_to_compare, r_all)
}
write.csv(r_all, paste0(base_path, "results.csv"), row.names=FALSE)