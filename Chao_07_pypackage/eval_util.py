
def max_f1_eval(predict_result, test_data_label, predefine_threshold = None):
    res_for_return = {}

    counter = 0
    tp = 0.0
    fp = 0.0
    fn = 0.0
    tn = 0.0

    for i, t in enumerate(predict_result):

        if t > 0.5:
            guess = True
        else:
            guess = False
        label = test_data_label[i]
        # print guess, label
        if guess == True and label == False:
            fp += 1.0
        elif guess == False and label == True:
            fn += 1.0
        elif guess == True and label == True:
            tp += 1.0
        elif guess == False and label == False:
            tn += 1.0
        if label == guess:
            counter += 1.0
        # else:
        # print label+'--'*20
        # if guess:
        # print "GOLD-" + str(label) + "\t" + "SYS-" + str(guess) + "\t" + sent1 + "\t" + sent2

    try:
        P = tp / (tp + fp)
        R = tp / (tp + fn)
        F = 2 * P * R / (P + R)
    except:
        P = 0
        R = 0
        F = 0

    # print("at threshold {}, precision: {}, recall: {}, F1: {}".format(0.5, P,R,F))
    res_for_return["f1"] = {"threshold":0.5, "precision":P, "recall":R, "f1":F}
    #print "PRECISION: %s, RECALL: %s, F1: %s" % (P, R, F)
    #print "ACCURACY: %s" % (counter / len(predict_result))

    counter = 0
    tp = 0.0
    fp = 0.0
    fn = 0.0
    tn = 0.0
    
    if predefine_threshold == None:
        predefine_threshold = 0.5
        
    for i, t in enumerate(predict_result):

        
        
        if t > predefine_threshold:
            guess = True
        else:
            guess = False
        label = test_data_label[i]
        # print guess, label
        if guess == True and label == False:
            fp += 1.0
        elif guess == False and label == True:
            fn += 1.0
        elif guess == True and label == True:
            tp += 1.0
        elif guess == False and label == False:
            tn += 1.0
        if label == guess:
            counter += 1.0
        # else:
        # print label+'--'*20
        # if guess:
        # print "GOLD-" + str(label) + "\t" + "SYS-" + str(guess) + "\t" + sent1 + "\t" + sent2

    try:
        P = tp / (tp + fp)
        R = tp / (tp + fn)
        F = 2 * P * R / (P + R)
    except:
        P = 0
        R = 0
        F = 0
        
    # print("at pre-defined threshold, tp is {}".format(tp))
#     print("tp: {}, fp: {}, fn: {}".format(tp,fp,fn))

    #print "PRECISION: %s, RECALL: %s, F1: %s" % (P, R, F)
    #print "ACCURACY: %s" % (counter / len(predict_result))

    # print "# true pos:", tp
    # print "# false pos:", fp
    # print "# false neg:", fn
    # print "# true neg:", tn
    maxF1 = 0
    P_maxF1 = 0
    R_maxF1 = 0
    p_list = []
    r_list = []
    f1_list = []
    thres_maxF1 = 0
    
    truepos_maxf1 = 0
    falsepos_maxf1 = 0
    
    probs = predict_result
    sortedindex = sorted(range(len(probs)), key=probs.__getitem__)
    sortedindex.reverse() #from big to small
    
#     print(probs[sortedindex[0]], probs[sortedindex[1]], probs[sortedindex[2]])
#     print(sortedindex)

    truepos = 0
    falsepos = 0
    for sortedi_idx, sortedi in enumerate(sortedindex):
        
#         print("A", predict_result[sortedi])
#         print("B", sortedindex[sortedi_idx + 1])
#         print("C", predict_result[sortedindex[sortedi_idx + 1]])
        
        
        
        if test_data_label[sortedi] == True:
            truepos += 1
        elif test_data_label[sortedi] == False:
            falsepos += 1
            
        # if several equal probs, I only look at the last one, skip all previous equal probs
        if sortedi_idx < len(sortedindex) - 1 and predict_result[sortedi] == predict_result[sortedindex[sortedi_idx + 1]]:
            continue
            
        precision = 0
        if truepos + falsepos > 0:
            precision = truepos * 1.0 / (truepos + falsepos)
        #print(precision)
        recall = truepos * 1.0 / (tp + fn)
        #print(recall)
        #print precision, recall
        f1 = 0
        if precision + recall > 0:
            
            
            
            f1 = 2 * precision * recall / (precision + recall)
            
            
            
            
            p_list.append(precision)
            r_list.append(recall)
            f1_list.append(f1)
            
            if f1 > maxF1:
                # print probs[sortedi]
                maxF1 = f1
                P_maxF1 = precision
                R_maxF1 = recall
#                 thres_maxF1 = predict_result[sortedi]
                thres_maxF1 = predict_result[sortedindex[sortedi_idx + 1]] 
                truepos_maxf1 = truepos
                falsepos_maxf1 = falsepos
                
            

    # print("at pre-defined threshold {}, precision: {}, recall: {}, F1: {}".format(predefine_threshold, P,R,F))
    # print("max F1 precision: {}, max F1 recall: {}, max F1: {}, threshold is {}".format(P_maxF1,R_maxF1,maxF1, thres_maxF1))
    # print("max f1 tp: {}, max f1 fp: {}, tp + fn: {}".format(truepos_maxf1,falsepos_maxf1,tp + fn))
    res_for_return["f1_at_pre-defined_threshold"] = {"threshold":predefine_threshold, "precision":P, "recall":R, "f1":F, "tp":tp, 'fp':fp, 'fn':fn}
    res_for_return["max_f1"] = {"threshold":thres_maxF1, "precision":P_maxF1, "recall":R_maxF1, "f1":maxF1, "tp":truepos_maxf1, 'fp':falsepos_maxf1, 'fn':tp+fn - truepos_maxf1 }

    # res_for_return.append([thres_maxF1, P_maxF1,R_maxF1,maxF1])
    # res_for_return.append([predefine_threshold, P,R,F])
    
    return res_for_return
    # return ((thres_maxF1, P_maxF1, R_maxF1, maxF1), (P,R,F))


def f1_eval(predict_result, test_data_label, predefine_threshold = None):
    res_for_return = {}

    counter = 0
    tp = 0.0
    fp = 0.0
    fn = 0.0
    tn = 0.0

    for i, t in enumerate(predict_result):

        if t > 0.5:
            guess = True
        else:
            guess = False
        label = test_data_label[i]
        # print guess, label
        if guess == True and label == False:
            fp += 1.0
        elif guess == False and label == True:
            fn += 1.0
        elif guess == True and label == True:
            tp += 1.0
        elif guess == False and label == False:
            tn += 1.0
        if label == guess:
            counter += 1.0
        # else:
        # print label+'--'*20
        # if guess:
        # print "GOLD-" + str(label) + "\t" + "SYS-" + str(guess) + "\t" + sent1 + "\t" + sent2

    try:
        P = tp / (tp + fp)
        R = tp / (tp + fn)
        F = 2 * P * R / (P + R)
    except:
        P = 0
        R = 0
        F = 0

    # print("at threshold {}, precision: {}, recall: {}, F1: {}".format(0.5, P,R,F))
    res_for_return["f1"] = {"threshold":0.5, "precision":P, "recall":R, "f1":F}
    #print "PRECISION: %s, RECALL: %s, F1: %s" % (P, R, F)
    #print "ACCURACY: %s" % (counter / len(predict_result))

    counter = 0
    tp = 0.0
    fp = 0.0
    fn = 0.0
    tn = 0.0
    
    if predefine_threshold == None:
        predefine_threshold = 0.5
        
    for i, t in enumerate(predict_result):

        
        
        if t > predefine_threshold:
            guess = True
        else:
            guess = False
        label = test_data_label[i]
        # print guess, label
        if guess == True and label == False:
            fp += 1.0
        elif guess == False and label == True:
            fn += 1.0
        elif guess == True and label == True:
            tp += 1.0
        elif guess == False and label == False:
            tn += 1.0
        if label == guess:
            counter += 1.0
        # else:
        # print label+'--'*20
        # if guess:
        # print "GOLD-" + str(label) + "\t" + "SYS-" + str(guess) + "\t" + sent1 + "\t" + sent2

    try:
        P = tp / (tp + fp)
        R = tp / (tp + fn)
        F = 2 * P * R / (P + R)
    except:
        P = 0
        R = 0
        F = 0
        
    # print("at pre-defined threshold, tp is {}".format(tp))
#     print("tp: {}, fp: {}, fn: {}".format(tp,fp,fn))

            

    # print("at pre-defined threshold {}, precision: {}, recall: {}, F1: {}".format(predefine_threshold, P,R,F))
    # print("max F1 precision: {}, max F1 recall: {}, max F1: {}, threshold is {}".format(P_maxF1,R_maxF1,maxF1, thres_maxF1))
    # print("max f1 tp: {}, max f1 fp: {}, tp + fn: {}".format(truepos_maxf1,falsepos_maxf1,tp + fn))
    res_for_return["f1_at_pre-defined_threshold"] = {"threshold":predefine_threshold, "precision":P, "recall":R, "f1":F, "tp":tp, 'fp':fp, 'fn':fn}

    # res_for_return.append([thres_maxF1, P_maxF1,R_maxF1,maxF1])
    # res_for_return.append([predefine_threshold, P,R,F])
    
    return res_for_return
    # return ((thres_maxF1, P_maxF1, R_maxF1, maxF1), (P,R,F))


