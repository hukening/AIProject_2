key_list = [];
true_table_all = []
class BasicModelChecking:
    # true_table=''
    # model_all={}
    def PL_TRUE(self, sentences=[], model={}):
        if (len(sentences) == 1):
            if (len(sentences[0]) <= 2):
                return model[sentences[0]];
        for sentence in sentences:
            '''
            if(len(sentence) <= 2):
                if(not model[sentence]):
                    return False;
                else:
                    continue;
            '''
            if (len(sentence) <= 2):
                if (not model[sentence]):
                    return False;
                else:
                    continue;
            A = '';
            B = '';
            connective = '';
            symbol_not = False;
            if (sentence[0] == '('):
                count = 1;
                pos = 0;
                for index in range(1, len(sentence)):
                    if (sentence[index] == '('):
                        count += 1;
                    if (sentence[index] == ')'):
                        count -= 1;
                    if (count == 0):
                        pos = index;
                        break;
                A = sentence[1:pos];
                connective = sentence[pos + 1];
                B = sentence[pos + 2:];
            if (sentence[0] == '~' and sentence[1] == '('):
                count = 1;
                pos = 0;
                for index in range(2, len(sentence)):
                    if (sentence[index] == '('):
                        count += 1;
                    if (sentence[index] == ')'):
                        count -= 1;
                    if (count == 0):
                        pos = index;
                        break;
                A = sentence[2:pos];
                connective = sentence[pos + 1];
                B = sentence[pos + 2:];
                symbol_not = True;
            if (sentence[0] == '~' and sentence[1] != '('):
                A = sentence[:2];
                connective = sentence[2];
                B = sentence[3:];
            else:
                A = sentence[0];
                connective = sentence[1];
                B = sentence[2:];

            l1 = [A];
            l2 = [B];
            bool_A = self.PL_TRUE(l1, model);
            bool_B = self.PL_TRUE(l2, model);
            #            bool_AB = True;
            if (symbol_not):
                bool_A = not bool_A;
            if (connective == '&'):
                if (not bool_A or not bool_B):
                    return False;
            if (connective == '|'):
                if (not bool_A and not bool_B):
                    return False;
            if (connective == '#'):
                if (bool_A and not bool_B):
                    return False;
            if (connective == '$'):
                if (not bool_A and bool_B):
                    return False;
                if (not bool_B and bool_A):
                    return False;
        return True;




    def TT_Entail(self, knowledge_base=[], beta=[]):
        print_symbols=''


        symbols = [];
        tmp = knowledge_base.copy();
        tmp += beta;
        for sentence in tmp:
            for char in sentence:
                if char >= 'A' and char <= 'Z':
                    if char not in symbols:
                        symbols.append(char);

        #self.true_table=symbols.copy()


        return self.TT_Check_All(knowledge_base, beta, symbols, {});


    def TT_Check_All(self, knowledge_base=[], beta=[], symbols=[], model={}):
        true_table_all=[]
        true_table_line=[]
        count=0
        if (len(symbols) == 0):
            # key_list.clear();
            # self.model_all=model
            # bool = True;
            # for key,value in model.items():
            #     key_list.append(key);
            #
            #     true_table_line.append(value)
            #     count+=1
            #     if count==model.__len__():
            #         true_table_all.append(true_table_line)
            # print(true_table_all)

            if (self.PL_TRUE(knowledge_base, model)):
                return self.PL_TRUE(beta, model);
            else:
                return True;

        P = symbols[0];
        rest = symbols[1:];

        model_1 = model.copy();
        model_2 = model.copy();
        model_1[P] = True;

        model_1["~" + P] = False;
        model_2[P] = False;
        model_2["~" + P] = True;

        #        print(model_1," ",self.TT_Check_All(knowledge_base,beta,rest,model_1)," 1");
        #        print(model_2," ",self.TT_Check_All(knowledge_base,beta,rest,model_2)," 2");
        return self.TT_Check_All(knowledge_base, beta, rest, model_1) and self.TT_Check_All(knowledge_base, beta, rest,
                                                                                            model_2);


alphas=[]
betas=[]
def read(filename):
    a=True
    alpha=[]
    beta=[]
    file=open(filename)
    for line in file.readlines():
        if line=="\n":
            a=False
            continue
        if a:
            alpha.append(line[:line.__len__()-1])
        else:
            beta.append(line[:line.__len__()-1])

    # print(knowledgebase)
    # print(beta)
    return alpha, beta

for file in range(8):
    filename=str(file+1)+'.txt'
    alpha, beta = read(filename)
    alphas.append(alpha)
    betas.append(beta)



for i in range(8):
    alpha = alphas[i];
    beta = betas[i];
    a = BasicModelChecking()
    print("sample ",i+1);


    for new_beta in beta:

        if (a.TT_Entail(alpha, [new_beta])):

            print(new_beta,":True");
           # print(key_list)
        if (not a.TT_Entail(alpha, [new_beta])):
            print(new_beta,":False");
            #print(key_list)



