#!/usr/bin/python3

class PriceDeterminer:

  def __init__(self):
    self.fixcostdict = {}
    self.percentcostsdict = {}
    self._total_fixcosts = None
    self._total_percentcosts = None
    self._total_variable_costs = None
    self._price = None

  def update_percentcostsdict(self, percentsdict):
    self._total_percentcosts = None
    self._price = None
    self.percentcostsdict.update(percentsdict)

  def update_fixcostdict(self, costdict):
    self._total_fixcosts = None
    self._price = None
    self.fixcostdict.update(costdict)

  def calculate_total_fixcosts(self):
    self._total_fixcosts = 0
    for costkey in self.fixcostdict:
      self._total_fixcosts += self.fixcostdict[costkey]

  @property
  def total_fixcosts(self):
    if self._total_fixcosts:
      return self._total_fixcosts
    self.calculate_total_fixcosts()
    return self._total_fixcosts

  def calculate_total_percentcosts(self):
    self._total_percentcosts = 0
    for percentkey in self.percentcostsdict:
      self._total_percentcosts += self.percentcostsdict[percentkey]

  @property
  def total_percentcosts(self):
    if self._total_percentcosts:
      return self._total_percentcosts
    self.calculate_total_percentcosts()
    return self._total_percentcosts

  @property
  def price(self):
    if self.total_fixcosts is None or self.total_percentcosts is None:
      return None
    if self._price is None:
      self.calculate_price()
    return self._price

  def calculate_price(self):
      self._price = self.total_fixcosts / (1 - self.total_percentcosts)

  @property
  def total_variable_costs(self):
    if self.price is None:
      return None
    if self._total_variable_costs is None:
      self.calculate_total_variable_costs()
    return self._total_variable_costs

  def calculate_total_variable_costs(self):
    self._total_variable_costs = 0
    for percentkey in self.percentcostsdict:
      self._total_variable_costs += self.percentcostsdict[percentkey] * self._price
    return self._total_variable_costs

  def recompose_price(self):
    recomposed = self.total_fixcosts + self.total_variable_costs
    print('recomposed', recomposed)
    print('Preço (fixos mais variáveis):', self.price)

  def __str__(self):
    outstr = 'PriceDeterminer\n'
    outstr += '='*50 + '\n'
    outstr += ':: Custos Fixos\n'
    for costkey in self.fixcostdict:
      outstr += ' %s => R$%0.2f\n' %(costkey, self.fixcostdict[costkey])
    outstr += '-'*50 + '\n'
    outstr += ' :: Subtotal custos fixos: R$%0.2f\n' %self.total_fixcosts
    outstr += '-'*50 + '\n'
    outstr += ':: Custos Variáveis\n'
    for percentkey in self.percentcostsdict:
      value = self.percentcostsdict[percentkey] * float(self.price)
      outstr += ' %s => R$%0.2f (percent %0.0fpc)\n' %(percentkey, float(value), self.percentcostsdict[percentkey]*100)
    outstr += '-'*50 + '\n'
    outstr += ' :: Subtotal custos variáveis: R$%0.2f (%0.0fpc)\n' %(self.total_variable_costs, self.total_percentcosts)
    outstr += '='*50 + '\n'
    outstr += ' => Preço (fixos mais variáveis): R$%0.2f\n' %(self.price)
    return outstr

def adhoc_test():
  pricer = PriceDeterminer()
  percentsdict = {'COMMIS1':0.1}
  pricer.update_percentcostsdict(percentsdict)
  percentsdict = {'COMMIS2':0.12}
  pricer.update_percentcostsdict(percentsdict)
  percentsdict = {'ICMS':0.15}
  pricer.update_percentcostsdict(percentsdict)
  percentsdict = {'COST var-financ':0.02}
  pricer.update_percentcostsdict(percentsdict)
  fixcostdict = {'COST matéria prima t-shirt':10}
  pricer.update_fixcostdict(fixcostdict)
  fixcostdict = {'COST fix-financ':1}
  pricer.update_fixcostdict(fixcostdict)
  fixcostdict = {'COST3 postmail':4}
  pricer.update_fixcostdict(fixcostdict)
  fixcostdict = {'Rateio médio despesa energia':5}
  pricer.update_fixcostdict(fixcostdict)
  fixcostdict = {'Rateio médio despesa aluguel':7}
  pricer.update_fixcostdict(fixcostdict)
  print(pricer)
  pricer.recompose_price()

def process():
  adhoc_test()

if __name__ == '__main__':
  process()
