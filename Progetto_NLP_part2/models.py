import torch.nn as nn 
from transformers import BertModel
import torch

class BertForRegression(nn.Module): 
        def __init__(self, drop_rate=0.2, freeze_camembert=False):           
            super(BertForRegression, self).__init__()
            D_in, D_out = 768, 1
        
            self.bert = BertModel.from_pretrained("bert-base-cased")

            self.regressor = nn.Sequential(
                nn.Dropout(drop_rate),
                nn.Linear(D_in, D_out))
        def forward(self, input_ids, token_type_ids, attention_mask):
        
            outputs = self.bert(input_ids, token_type_ids, attention_mask)
            class_label_output = outputs[1]
            outputs = self.regressor(class_label_output)
            return outputs
        
class BertForRegressionSigmoid(nn.Module): 
        def __init__(self, drop_rate=0.2, freeze_camembert=False):           
            super(BertForRegressionSigmoid, self).__init__()
            D_in, D_out = 768, 1
        
            self.bert = BertModel.from_pretrained("bert-base-cased")

            self.regressor = nn.Sequential(
                nn.Dropout(drop_rate),
                nn.Linear(D_in, D_out))
        def forward(self, input_ids, token_type_ids, attention_mask):
            
            outputs = self.bert(input_ids, token_type_ids, attention_mask)
            class_label_output = outputs.pooler_output
            f = nn.Sigmoid()
            outputs = f(self.regressor(class_label_output))
            return outputs        
        
class BertForClassification(nn.Module): 
        def __init__(self, num_classes, drop_rate=0.2, freeze_camembert=False):           
            super(BertForClassification, self).__init__()
            D_in, D_out = 768, num_classes
        
            self.bert = BertModel.from_pretrained("bert-base-cased")

            self.classifier = nn.Sequential(
                nn.Dropout(drop_rate),
                nn.Linear(D_in, D_out))
        def forward(self, input_ids, token_type_ids, attention_mask):
        
            outputs = self.bert(input_ids, token_type_ids, attention_mask)
            class_label_output = outputs.pooler_output
            outputs = self.classifier(class_label_output)
            return outputs
        
class Wrapper(nn.Module):
    def __init__(self, model):
        super(Wrapper,self).__init__()
        self.model = model
    def forward(self, arg):
        return self.model(arg, torch.LongTensor([[0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]]) , torch.LongTensor([[1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1, 1]]))
    
class Prova(nn.Module):
    def __init__(self, model):
        super(Prova, self).__init__()
        self.model = model
        self.classifier = nn.Sequential(
            nn.Dropout(0.2),
            nn.Linear(50257, 1))
    def forward(self, input_ids):
        outputs = self.model(input_ids)
        outputs= self.classifier(outputs.logits)
        return outputs

    
        